from rest_framework import viewsets, generics, status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import action
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
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), (IsSuperAdmin | IsOfficeAdmin)]
        return [permissions.IsAuthenticated(), (IsSuperAdmin | IsOfficeAdmin)]

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
             return [permissions.IsAuthenticated(), (IsEmployee | IsSuperAdmin | IsOfficeAdmin)]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Allow unrestricted access for check_status via its own logic, 
        # but for list/retrieve, restrict based on role.
        if self.action == 'check_status':
            return Token.objects.all()

        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'profile'):
             return Token.objects.none()

        if user.profile.role == 'SUPERADMIN':
            return Token.objects.all()
        elif user.profile.role == 'OFFICEADMIN':
            return Token.objects.filter(office=user.profile.assigned_office)
        elif user.profile.role == 'EMPLOYEE':
             try:
                 if user.profile.assigned_office:
                     return Token.objects.filter(office=user.profile.assigned_office)
                 return Token.objects.none()
             except:
                 return Token.objects.none()
        elif user.profile.role == 'CUSTOMER':
            return Token.objects.filter(customer=user)
        return Token.objects.none()

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
