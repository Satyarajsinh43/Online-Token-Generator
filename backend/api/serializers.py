from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Token, District, Taluka, Village, Office, Profile, Employee, Service

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        if hasattr(user, 'profile'):
             token['role'] = user.profile.role
             if user.profile.assigned_office:
                 token['office_id'] = user.profile.assigned_office.id

        return token

# --- Geography Serializers ---
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class TalukaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taluka
        fields = '__all__'

class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'

# --- Core Business Serializers ---
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class OfficeSerializer(serializers.ModelSerializer):
    district_name = serializers.ReadOnlyField(source='district.name')
    taluka_name = serializers.ReadOnlyField(source='taluka.name')
    # Village might be null for Urban
    village_name = serializers.ReadOnlyField(source='village.name')

    class Meta:
        model = Office
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    office_name = serializers.ReadOnlyField(source='assigned_office.office_name')
    
    class Meta:
        model = Profile
        fields = ('role', 'assigned_office', 'office_name')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True, required=False) 
    assigned_office = serializers.PrimaryKeyRelatedField(queryset=Office.objects.all(), write_only=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'profile', 'role', 'assigned_office')

    def create(self, validated_data):
        role = validated_data.pop('role', 'CUSTOMER')
        assigned_office = validated_data.pop('assigned_office', None)
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user)
            
        profile.role = role
        if assigned_office:
            profile.assigned_office = assigned_office
        profile.save()
        
        return user

class EmployeeSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    office_name = serializers.ReadOnlyField(source='office.office_name')

    class Meta:
        model = Employee
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    office_name = serializers.ReadOnlyField(source='office.office_name')
    generated_by_name = serializers.ReadOnlyField(source='generated_by.user.user_name')
    customer_username = serializers.ReadOnlyField(source='customer.username')
    verified_by_name = serializers.ReadOnlyField(source='verified_by.first_name')
    
    district_name = serializers.ReadOnlyField(source='district.name')
    taluka_name = serializers.ReadOnlyField(source='taluka.name')
    village_name = serializers.ReadOnlyField(source='village.name')

    class Meta:
        model = Token
        fields = '__all__'
        # These fields are read-only because they are set by backend logic or reference models
        read_only_fields = ('token_number', 'created_at', 'updated_at', 'status', 'generated_by', 'customer', 
                            'district', 'taluka', 'village', 'rural_or_urban', 'verified_by', 'verified_at')

class TokenStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('status',)

class BookTokenSerializer(serializers.ModelSerializer):
    """
    Serializer to validate incoming booking requests.
    """
    district_id = serializers.IntegerField()
    taluka_id = serializers.IntegerField(required=False, allow_null=True)
    village_id = serializers.IntegerField(required=False, allow_null=True)
    office_id = serializers.IntegerField()
    service_id = serializers.IntegerField()
    booking_date = serializers.DateField()
    slot_time = serializers.TimeField()

    class Meta:
        model = Token
        fields = ['customer_name', 'customer_phone', 'district_id', 'taluka_id', 'village_id', 'office_id', 'service_id', 'booking_date', 'slot_time']
