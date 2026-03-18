from django.contrib import admin
from .models import District, Taluka, Village, Office, Token, Employee, Profile

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Taluka)
class TalukaAdmin(admin.ModelAdmin):
    list_display = ('name', 'district')
    list_filter = ('district',)
    search_fields = ('name',)

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'taluka')
    list_filter = ('taluka__district', 'taluka')
    search_fields = ('name',)

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('office_name', 'office_code', 'office_type', 'district', 'taluka', 'village')
    list_filter = ('office_type', 'district', 'taluka')
    search_fields = ('office_name', 'office_code')

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('token_number', 'customer_name', 'status', 'office', 'created_at')
    list_filter = ('status', 'office__district', 'office__office_type', 'created_at')
    search_fields = ('token_number', 'customer_name', 'mobile_number')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'office', 'active_status')
    list_filter = ('office', 'active_status')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'assigned_office')
    list_filter = ('role',)
