from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """
    Allocates Full Access to SuperAdmin
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                hasattr(request.user, 'profile') and 
                request.user.profile.role == 'SUPERADMIN')

class IsOfficeAdmin(permissions.BasePermission):
    """
    Allocates Access to OfficeAdmin for their own office
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                hasattr(request.user, 'profile') and 
                request.user.profile.role == 'OFFICEADMIN')

    def has_object_permission(self, request, view, obj):
        # Check if the object belongs to the admin's office
        # Assumes obj has 'office' attribute or is 'Office' itself
        if hasattr(obj, 'office'):
            return obj.office == request.user.profile.assigned_office
        if hasattr(obj, 'id'): # If obj is Office instance
             # This check depends on the model type, handling in ViewSet is safer but this provides granular check
             return obj == request.user.profile.assigned_office
        return False

class IsEmployee(permissions.BasePermission):
    """
    Allocates Access to Employee for their own office
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                hasattr(request.user, 'profile') and 
                request.user.profile.role == 'EMPLOYEE')

class IsCustomer(permissions.BasePermission):
    """
    Allocates Access to Customer
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                hasattr(request.user, 'profile') and 
                request.user.profile.role == 'CUSTOMER')
