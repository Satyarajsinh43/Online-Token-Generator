from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- Geography Models ---

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, help_text="District Code (e.g., GJ01)")
    rto_code = models.CharField(max_length=5, blank=True, null=True, help_text="RTO Code (e.g., 01 for Ahmedabad)")
    
    def __str__(self):
        return self.name

class Taluka(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, related_name='talukas', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'district')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.district.name})"

class Village(models.Model):
    name = models.CharField(max_length=100)
    taluka = models.ForeignKey(Taluka, related_name='villages', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'taluka')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.taluka.name})"

# --- Core Business Models ---

class Office(models.Model):
    OFFICE_TYPE_CHOICES = (
        ('URBAN', 'Urban'),
        ('RURAL', 'Rural'),
        ('RTO', 'Regional Transport Office'),
    )
    office_name = models.CharField(max_length=100)
    office_code = models.CharField(max_length=50, unique=True, help_text="Unique Office Code")
    office_type = models.CharField(max_length=10, choices=OFFICE_TYPE_CHOICES)
    token_sequence_code = models.CharField(max_length=2, default='A', help_text="Code for token generation (e.g., A, B)")
    
    # Location Hierarchy - Nullable to allow migration from previous schema
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True, help_text="Required if Rural")
    
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        loc = self.taluka.name if self.office_type == 'URBAN' and self.taluka else (self.village.name if self.village else 'Unknown')
        return f"{self.office_name} ({self.office_type} - {loc})"

class Profile(models.Model):
    ROLE_CHOICES = (
        ('SUPERADMIN', 'SuperAdmin'),
        ('OFFICEADMIN', 'OfficeAdmin'),
        ('EMPLOYEE', 'Employee'),
        ('CUSTOMER', 'Customer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')
    assigned_office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, blank=True, help_text="For OfficeAdmin and Employee")
    assigned_district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, help_text="For District-level view access")

    def __str__(self):
        return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile') # Link to Auth User
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='employees')
    designation = models.CharField(max_length=100)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.designation} at {self.office.office_name}"

class Service(models.Model):
    name = models.CharField(max_length=100)
    office_type = models.CharField(max_length=10) # We will validate against Office types in logic or choices if needed
    avg_time_minutes = models.IntegerField(default=15, help_text="Average time in minutes")

    def __str__(self):
        return f"{self.name} ({self.office_type})"

class Token(models.Model):
    STATUS_CHOICES = [
        ('WAITING', 'Waiting'),
        ('VERIFIED', 'Verified'),
        ('SERVING', 'Serving'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    OFFICE_TYPE_CHOICES = (
        ('URBAN', 'Urban'),
        ('RURAL', 'Rural'),
    )

    token_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # Blockchain Details
    token_hash = models.CharField(max_length=256, unique=True, null=True, blank=True)
    blockchain_tx = models.CharField(max_length=256, null=True, blank=True)
    
    # Store complete hierarchy for reporting
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    taluka = models.ForeignKey(Taluka, on_delete=models.SET_NULL, null=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True)
    office = models.ForeignKey(Office, related_name='tokens', on_delete=models.CASCADE)
    rural_or_urban = models.CharField(max_length=10, choices=OFFICE_TYPE_CHOICES, default='RURAL')

    # Customer Data
    customer_name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    customer_phone = models.CharField(max_length=15, blank=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_tokens', help_text="Registered customer account")
    generated_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_tokens', help_text="If generated by employee manually")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WAITING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    
    # Slot-based booking additions
    booking_date = models.DateField(null=True, blank=True)
    slot_time = models.TimeField(null=True, blank=True)
    
    # Verification System
    verified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='verified_tokens')
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['token_number']),
            models.Index(fields=['office', 'created_at']),
        ]

    def __str__(self):
        return f"{self.token_number} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.token_number:
            from django.db import transaction, IntegrityError
            from django.utils import timezone
            
            # Get RTO Code
            rto_code = "00"
            if self.district and self.district.rto_code:
                rto_code = self.district.rto_code
            
            # Get Office Sequence Code
            office_seq = "A"
            if self.office:
                office_seq = self.office.token_sequence_code
            
            prefix = f"GJ{rto_code}{office_seq}"
            today = timezone.now().date()
            
            # Retry loop for concurrent insertions
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    with transaction.atomic():
                        # Find the highest sequence number for this prefix
                        last_token = Token.objects.filter(
                            token_number__startswith=prefix
                        ).order_by('created_at').select_for_update().last()
                        
                        if last_token:
                            try:
                                # Extract sequence by replacing the prefix
                                seq_str = last_token.token_number.replace(prefix, "")
                                last_seq = int(seq_str)
                                new_seq = last_seq + 1
                            except ValueError:
                                new_seq = 1
                        else:
                            new_seq = 1
                        
                        self.token_number = f"{prefix}{new_seq:03d}"
                        return super(Token, self).save(*args, **kwargs)
                except IntegrityError:
                    if attempt == max_retries - 1:
                        raise # Give up after max retries
                    continue # Try again
        else:
            super(Token, self).save(*args, **kwargs)

class OTPVerification(models.Model):
    contact = models.CharField(max_length=100) # Email or Phone
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def is_expired(self):
        from django.utils import timezone
        import datetime
        return timezone.now() > self.created_at + datetime.timedelta(minutes=5)
    
    def __str__(self):
        return f"{self.contact} - {self.otp} - Verified: {self.is_verified}"
