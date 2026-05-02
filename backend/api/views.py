from rest_framework import viewsets, generics, status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Office, Token, Employee, Profile, District, Taluka, Village, Service, OTPVerification
from .serializers import (
    UserSerializer, OfficeSerializer, EmployeeSerializer, 
    TokenSerializer, TokenStatusUpdateSerializer,
    DistrictSerializer, TalukaSerializer, VillageSerializer,
    MyTokenObtainPairSerializer, ServiceSerializer
)
from .permissions import IsSuperAdmin, IsOfficeAdmin, IsEmployee, IsCustomer
import random
import string
from django.utils import timezone
from .blockchain_utils import generate_token_hash, store_token_hash_on_blockchain

# --- Auth Views ---
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

# --- Geography Views ---

class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all().order_by('name')
    serializer_class = DistrictSerializer
    permission_classes = [permissions.AllowAny]

class TalukaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Taluka.objects.select_related('district').all().order_by('name')
    serializer_class = TalukaSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        district_id = self.request.query_params.get('district')
        if district_id:
            queryset = queryset.filter(district_id=district_id)
        return queryset

class VillageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Village.objects.select_related('taluka').all().order_by('name')
    serializer_class = VillageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        taluka_id = self.request.query_params.get('taluka')
        if taluka_id:
            queryset = queryset.filter(taluka_id=taluka_id)
        return queryset

# --- Core Business Views ---

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all().order_by('name')
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        office_type = self.request.query_params.get('office_type')
        if office_type:
            queryset = queryset.filter(office_type=office_type)
        return queryset

from .pagination import StandardResultsSetPagination

class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.select_related('district', 'taluka', 'village').all().order_by('office_name')
    serializer_class = OfficeSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Helper to safely get int params
        def get_int_param(name):
            try:
                val = self.request.query_params.get(name)
                return int(val) if val else None
            except (ValueError, TypeError):
                return None

        district_id = get_int_param('district')
        taluka_id = get_int_param('taluka')
        village_id = get_int_param('village')
        office_type = self.request.query_params.get('office_type')

        if district_id:
            queryset = queryset.filter(district_id=district_id)
        if taluka_id:
            queryset = queryset.filter(taluka_id=taluka_id)
        if village_id:
            queryset = queryset.filter(village_id=village_id)
        if office_type:
            queryset = queryset.filter(office_type=office_type)
            
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSuperAdmin()]
        return [permissions.AllowAny()]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated, IsSuperAdmin | IsOfficeAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'profile'):
            return Employee.objects.none()
            
        if user.profile.role == 'SUPERADMIN':
            return Employee.objects.all()
        elif user.profile.role == 'OFFICEADMIN':
            return Employee.objects.filter(office=user.profile.assigned_office)
        else:
            return Employee.objects.none()

    def perform_create(self, serializer):
        # Ensure OfficeAdmin can only add employees to their own office
        if self.request.user.profile.role == 'OFFICEADMIN':
            serializer.save(office=self.request.user.profile.assigned_office)
        else:
            serializer.save()

from rest_framework.views import APIView
from django.db import transaction

class CreateEmployeeAPIView(APIView):
    """
    Custom secure endpoint for Super Admins and Office Admins to create new staff.
    """
    permission_classes = [permissions.IsAuthenticated, (IsSuperAdmin | IsOfficeAdmin)]

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        office_id = data.get('office_id')
        designation = data.get('designation', 'Staff Member')

        if not email or not password:
            return Response({'error': 'Email and Password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Enforce OfficeAdmin restrictions (they can only assign to their own office)
        if user.profile.role == 'OFFICEADMIN':
            if not user.profile.assigned_office:
                return Response({'error': 'You are not assigned to an office.'}, status=status.HTTP_403_FORBIDDEN)
            office_id = user.profile.assigned_office.id

        if not office_id:
            return Response({'error': 'Office assignment is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            office = Office.objects.get(id=office_id)
        except Office.DoesNotExist:
            return Response({'error': 'Invalid Office ID.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
           return Response({'error': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # 1. Create User
                # Email is used as Username for login consistency
                new_user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_staff=True  # Staff members need this flag
                )

                # 2. Update Profile to EMPLOYEE
                profile, _ = Profile.objects.get_or_create(user=new_user)
                profile.role = 'EMPLOYEE'
                profile.assigned_office = office
                profile.save()

                # 3. Create Employee Record
                Employee.objects.create(
                    user=new_user,
                    office=office,
                    designation=designation
                )

            return Response({'message': 'Staff created successfully.'}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action == 'check_status':
            return [permissions.AllowAny()]
        if self.action in ['update', 'partial_update']:
             permission_classes = [permissions.IsAuthenticated, IsEmployee | IsSuperAdmin | IsOfficeAdmin]
             return [permission() for permission in permission_classes]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Auto-cancel outdated waiting tokens before returning
        Token.objects.filter(
            booking_date__lt=timezone.now().date(), 
            status='WAITING'
        ).update(status='CANCELLED')

        # Allow unrestricted access for check_status via its own logic, 
        # but for list/retrieve, restrict based on role.
        if self.action == 'check_status':
            return Token.objects.all()

        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'profile'):
             return Token.objects.none()

        queryset = Token.objects.none()
        if user.profile.role == 'SUPERADMIN':
            queryset = Token.objects.all()
        elif user.profile.role == 'OFFICEADMIN':
            queryset = Token.objects.filter(office=user.profile.assigned_office)
        elif user.profile.role == 'EMPLOYEE':
             try:
                 if user.profile.assigned_district:
                     queryset = Token.objects.filter(office__district=user.profile.assigned_district)
                 elif user.profile.assigned_office:
                     queryset = Token.objects.filter(office=user.profile.assigned_office)
             except:
                 pass
        elif user.profile.role == 'CUSTOMER':
            queryset = Token.objects.filter(customer=user)

        booking_date = self.request.query_params.get('booking_date')
        if booking_date:
            queryset = queryset.filter(booking_date=booking_date)

        return queryset

    def create(self, request, *args, **kwargs):
        office_id = request.data.get('office')
        if not office_id:
             return Response({"error": "Office ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            office = Office.objects.get(id=office_id)
        except Office.DoesNotExist:
             return Response({"error": "Office not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate Token Number
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        token_number = f"{office.office_code}-{random_part}"
        
        while Token.objects.filter(token_number=token_number).exists():
             random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
             token_number = f"{office.office_code}-{random_part}"

        # Handle Customer
        customer = request.user if request.user.is_authenticated else None
        customer_name = request.data.get('customer_name')
        
        if not customer_name:
            if customer:
                customer_name = customer.first_name or customer.username
            else:
                 return Response({"error": "Customer Name is required for guest booking"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        
        # Validate slot capacity for TokenViewSet
        booking_date_str = request.data.get('booking_date')
        slot_time_str = request.data.get('slot_time')

        if booking_date_str and slot_time_str:
            try:
                count = Token.objects.filter(
                    booking_date=booking_date_str, 
                    slot_time=slot_time_str, 
                    office=office, 
                    status__in=['WAITING', 'SERVING', 'COMPLETED']
                ).count()
                if count >= 5:
                    return Response({"error": "Selected slot is full."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                pass

        # Populate new hierarchy fields from the selected Office
        token = Token.objects.create(
            token_number=token_number,
            customer=customer,
            office=office,
            
            # Store Hierarchy from Office
            district=office.district,
            taluka=office.taluka,
            village=office.village, # Nullable
            rural_or_urban=office.office_type,
            
            customer_name=customer_name,
            customer_phone=request.data.get('mobile_number'), # Map to new field
            mobile_number=request.data.get('mobile_number'), # redundant but keep
            email=request.data.get('email'),
            booking_date=booking_date_str,
            slot_time=slot_time_str,
            status='WAITING'
        )
        
        # Blockchain Integration
        timestamp_str = str(token.created_at.timestamp())
        token_hash = generate_token_hash(token.token_number, token.customer_name, str(token.office.id), timestamp_str)
        token.token_hash = token_hash
        # Note: Sending to blockchain can be slow. In production this should be a Celery task
        tx_hash = store_token_hash_on_blockchain(token_hash)
        if tx_hash:
             token.blockchain_tx = tx_hash
        token.save()
        
        return Response(TokenSerializer(token).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], serializer_class=TokenStatusUpdateSerializer)
    def update_status(self, request, pk=None):
        token = self.get_object()
        new_status = request.data.get('status')
        
        valid_statuses = [c[0] for c in Token.STATUS_CHOICES]
        if new_status not in valid_statuses:
             return Response({"error": f"Invalid status. Choices: {valid_statuses}"}, status=status.HTTP_400_BAD_REQUEST)

        token.status = new_status
        token.save()
        return Response(TokenSerializer(token).data)

    @action(detail=False, methods=['get'])
    def check_status(self, request):
        token_number = request.query_params.get('token_number')
        if not token_number:
            return Response({"error": "Token number is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            token = Token.objects.get(token_number=token_number)
            
            # Auto-cancel if outdated
            if token.booking_date and token.booking_date < timezone.now().date() and token.status == 'WAITING':
                token.status = 'CANCELLED'
                token.save()
                
            serializer = TokenSerializer(token)
            return Response(serializer.data)
        except Token.DoesNotExist:
            return Response({"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND)

from .pdf_utils import generate_token_receipt
from django.http import HttpResponse

class BookTokenView(generics.CreateAPIView):
    """
    API View to book a token.
    """
    serializer_class = TokenSerializer # Actually returns TokenSerializer
    permission_classes = [permissions.AllowAny] # Allow guests to book

    def post(self, request, *args, **kwargs):
        # Validate input using BookTokenSerializer (manual validation or separate serializer)
        # For simplicity, we can extract data directly or use the serializer we created
        from .serializers import BookTokenSerializer
        
        start_serializer = BookTokenSerializer(data=request.data)
        if not start_serializer.is_valid():
            return Response(start_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        data = start_serializer.validated_data
        
        try:
            office = Office.objects.get(id=data['office_id'])
            service = Service.objects.get(id=data['service_id'])
        except (Office.DoesNotExist, Service.DoesNotExist) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Validate slot capacity for BookTokenView
        booking_date_str = data.get('booking_date')
        slot_time_str = data.get('slot_time')

        if booking_date_str and slot_time_str:
            try:
                count = Token.objects.filter(
                    booking_date=booking_date_str, 
                    slot_time=slot_time_str, 
                    office=office, 
                    status__in=['WAITING', 'SERVING', 'COMPLETED']
                ).count()
                if count >= 5:
                    return Response({"error": "Selected slot is full."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                pass

        # Handle Customer (Auth or Guest)
        customer = request.user if request.user.is_authenticated else None
        
        # Create Token (save() method handles number generation)
        token = Token.objects.create(
            customer=customer,
            customer_name=data['customer_name'],
            customer_phone=data.get('customer_phone'),
            mobile_number=data.get('customer_phone'), # Redundant but safe
            
            office=office,
            service=service,
            
            district_id=data['district_id'],
            taluka_id=data.get('taluka_id'),
            village_id=data.get('village_id'),
            rural_or_urban=office.office_type,
            
            booking_date=booking_date_str,
            slot_time=slot_time_str,
            status='WAITING'
        )
        
        # Blockchain Integration
        timestamp_str = str(token.created_at.timestamp())
        token_hash = generate_token_hash(token.token_number, token.customer_name, str(token.office.id), timestamp_str)
        token.token_hash = token_hash
        # Note: Sending to blockchain can be slow. In production this should be a Celery task
        tx_hash = store_token_hash_on_blockchain(token_hash)
        if tx_hash:
             token.blockchain_tx = tx_hash
        token.save()
        
        # Return success with receipt URL
        response_data = TokenSerializer(token).data
        response_data['message'] = "Token booked successfully"
        response_data['receipt_url'] = f"/api/token/receipt/{token.id}/"
        
        return Response(response_data, status=status.HTTP_201_CREATED)

class TokenReceiptView(generics.RetrieveAPIView):
    """
    API View to download token receipt PDF.
    """
    queryset = Token.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk=None):
        token = get_object_or_404(Token, pk=pk)
        
        pdf_buffer = generate_token_receipt(token)
        
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Token_{token.token_number}.pdf"'
        return response

from .blockchain_utils import verify_token_on_blockchain

class VerifyTokenView(generics.GenericAPIView):
    """
    API View to verify token authenticity.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, token_hash=None):
        if not token_hash:
             return Response({"error": "Token hash is required"}, status=status.HTTP_400_BAD_REQUEST)
             
        try:
             token = Token.objects.get(token_hash=token_hash)
        except Token.DoesNotExist:
             return Response({"status": "Invalid", "message": "Token not found in database"}, status=status.HTTP_404_NOT_FOUND)
             
        # Optional: check if token exists on blockchain
        blockchain_valid = verify_token_on_blockchain(token_hash)
        
        response_data = {
            "status": "Valid" if blockchain_valid else "Warning",
            "message": "Token is authentic and verified on blockchain" if blockchain_valid else "Token found in database but not yet verified on blockchain",
            "token_number": token.token_number,
            "office_name": token.office.office_name,
            "service_name": token.service.name if token.service else "N/A",
            "customer_name": token.customer_name,
            "created_at": token.created_at.isoformat(),
            "blockchain_tx": token.blockchain_tx,
            "blockchain_verified": blockchain_valid
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class SendOTPView(generics.GenericAPIView):
    """
    API View to generate and send an OTP.
    Since frontend uses EmailJS for emails, for emails we just generate the OTP and return it.
    (In a production environment, sending emails/SMS should be done strictly in backend via Celery.)
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        contact = request.data.get('contact')
        if not contact:
            return Response({"error": "Contact (email or phone) is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate 6-digit OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        
        # Invalidate any previous unused OTPs for this contact
        OTPVerification.objects.filter(contact=contact, is_verified=False).delete()
        
        # Save to DB
        otp_record = OTPVerification.objects.create(
            contact=contact,
            otp=otp_code
        )
        
        # NOTE: If we wanted to send SMS directly from Django, we would trigger Fast2SMS here.
        # But we will return the OTP so the frontend can send it via EmailJS.
        # This is a bit insecure if public, but matches the requested EmailJS frontend flow.
        
        return Response({
            "message": "OTP generated successfully",
            "otp": otp_code # Returning OTP to frontend for EmailJS integration
        }, status=status.HTTP_201_CREATED)

class VerifyOTPView(generics.GenericAPIView):
    """
    API View to verify the OTP.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        contact = request.data.get('contact')
        otp_input = request.data.get('otp')
        
        if not contact or not otp_input:
            return Response({"error": "Contact and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # Get the latest OTP request for this contact
            otp_record = OTPVerification.objects.filter(contact=contact).latest('created_at')
        except OTPVerification.DoesNotExist:
            return Response({"error": "No OTP request found for this contact."}, status=status.HTTP_404_NOT_FOUND)
            
        if otp_record.is_verified:
            return Response({"error": "This OTP has already been verified."}, status=status.HTTP_400_BAD_REQUEST)
            
        if otp_record.is_expired():
            return Response({"error": "OTP has expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)
            
        if otp_record.otp != otp_input:
            # Optional: Implement attempt counter tracking here
            return Response({"error": "Invalid OTP code."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Success
        otp_record.is_verified = True
        otp_record.save()
        
        return Response({"verified": True, "message": "OTP verified successfully."}, status=status.HTTP_200_OK)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def clerk_sync_user(request):
    """
    Syncs the Clerk user with Django User and Profile.
    Called from frontend after successful Clerk authentication.
    """
    email = request.data.get('email')
    name = request.data.get('name') or ''
    first_name = request.data.get('first_name') or ''
    last_name = request.data.get('last_name') or ''
    
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        # Avoid MultipleObjectsReturned by taking the first match if multiple exist
        user = User.objects.filter(email=email).first()
        created = False
        if not user:
            # Handle username clashes safely
            username = email
            if User.objects.filter(username=username).exists():
                import uuid
                username = f"{email}_{str(uuid.uuid4())[:8]}"
            
            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name or name,
                last_name=last_name,
            )
            created = True
        
        # Ensure Profile exists
        profile, p_created = Profile.objects.get_or_create(user=user)
        if p_created:
            profile.role = 'CUSTOMER'
            profile.save()

        # Map to Gandhinagar automatically if specified staff email is detected
        if email.lower() == 'raiyaniprince7@gmail.com':
            profile.role = 'EMPLOYEE'
            # Look for the Gandhinagar district safely
            gdh_dist = District.objects.filter(name__icontains='gandhinagar').first()
            if gdh_dist:
                profile.assigned_district = gdh_dist
            profile.save()
            
            # Ensure an Employee record exists for Admin visibility
            if gdh_dist:
                office = Office.objects.filter(district=gdh_dist).first()
                if office and not hasattr(user, 'employee_profile'):
                    Employee.objects.create(
                        user=user,
                        office=office,
                        designation='Gandhinagar Staff'
                    )

        # Grant SUPERADMIN to developer emails
        if email.lower().startswith('admin@'):
            profile.role = 'SUPERADMIN'
            profile.save()
            
        # Optional: update name if it changed
        if not created and first_name:
             user.first_name = first_name
             user.last_name = last_name
             user.save()
             
        # Resolve district name for frontend Context usage safely
        district_name = None
        if profile.assigned_district:
            district_name = profile.assigned_district.name
        elif profile.assigned_office and profile.assigned_office.district:
            district_name = profile.assigned_office.district.name

        # Return user details need for AuthContext
        return Response({
            'message': 'User synced successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': profile.role,
                'assigned_office': profile.assigned_office.id if profile.assigned_office else None,
                'district_name': district_name,
            }
        }, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from datetime import datetime, timedelta, time
from django.db.models import Count

class AvailableSlotsView(APIView):
    """
    Returns available 15-minute slots for a given date and office.
    Capacity: 5 per slot.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        date_str = request.query_params.get('date')
        office_id = request.query_params.get('office_id')

        if not date_str or not office_id:
            return Response({"error": "date and office_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if booking_date < timezone.now().date():
                 return Response({"error": "Cannot book for past dates."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate 15 min slots from 09:00 to 16:45
        slots = []
        current_time = datetime.combine(booking_date, time(9, 0))
        end_time = datetime.combine(booking_date, time(17, 0))

        while current_time < end_time:
            slots.append(current_time.time())
            current_time += timedelta(minutes=15)

        # Count existing tokens for the given date and office, grouped by slot_time
        booked_counts = Token.objects.filter(
            booking_date=booking_date,
            office_id=office_id,
            status__in=['WAITING', 'SERVING', 'COMPLETED']
        ).values('slot_time').annotate(count=Count('id'))

        # Convert to dictionary { time_obj: count }
        count_dict = {item['slot_time']: item['count'] for item in booked_counts if item['slot_time']}

        response_data = []
        for slot in slots:
            count = count_dict.get(slot, 0)
            response_data.append({
                "time": slot.strftime('%H:%M'),
                "available": count < 5,
                "current_capacity": count
            })

        return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_token(request):
    user = request.user
    token_hash = request.data.get("token_hash")

    if not token_hash:
        return Response({"error": "Token hash is required"}, status=400)

    try:
        token = Token.objects.get(token_hash=token_hash)
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=404)

    # Check staff role
    if not hasattr(user, 'profile') or user.profile.role not in ['EMPLOYEE', 'SUPERADMIN', 'OFFICEADMIN']:
        return Response({"error": "Unauthorized"}, status=403)

    # Check district match for standard employees
    if user.profile.role == 'EMPLOYEE':
        has_access = False
        if user.profile.assigned_district and token.office.district == user.profile.assigned_district:
            has_access = True
        elif user.profile.assigned_office and token.office == user.profile.assigned_office:
            has_access = True
            
        if not has_access:
            return Response({"error": "Access denied"}, status=403)

    # Prevent re-verification
    if token.status != "WAITING":
        return Response({"error": "Token already used or cancelled. Current Status: " + token.status}, status=400)

    token.status = "VERIFIED"
    token.verified_by = user
    token.verified_at = timezone.now()
    token.save()

    return Response({
        "message": "Token verified successfully",
        "token_number": token.token_number
    })
