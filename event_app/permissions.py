from rest_framework.permissions import BasePermission


class RegisterPermission(BasePermission):
    def has_permission(self, request, view):

        if request.user.role in ['admin','supervisor']:
            return True
        return False


class PendingListPermission(BasePermission):

    def has_permission(self, request, view):

        

        if request.user.role=="employee":
            return True

        if request.user.role in ['admin','supervisor']:

            if request.method =="GET":
                return True

        return False

class DecisionPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.role=='supervisor':
            return True
        return False


class ProfilePermissions(BasePermission):


    def has_permission(self, request, view):

        if request.user.role=='supervisor':
            if request.method != 'POST':
                return True
        
        if request.user.role=='employee':
            if request.method != 'DELETE':
                return True
        return False

    
        
            