from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsCustomerReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            
            return True
        return False

class IsAdminOrSeller(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
        
        return(
            request.user.user_role in ['admin','seller'] and request.user.approval_status=='approved'
        )
    
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
        
        if request.user.user_role == 'admin' and request.user.is_staff:
            return True
        
        return(
            request.user.user_role=='seller' and request.user.approval_status=='approved' and obj.created_by == request.user
        )
            