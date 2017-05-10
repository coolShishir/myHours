from rest_framework.permissions import BasePermission

#custom permission class for admin user restrictions
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        print '--------', request.user.UserType
        if request.user and str(request.user.UserType) == 'A' :
            return True
        return False

#custom permission class for client user restrictions
class IsClient(BasePermission):
    def has_permission(self, request, view):
        print '--------', request.user.UserType
        if request.user and str(request.user.UserType) == 'C' :
            return True
        return False