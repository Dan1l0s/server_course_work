from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            if request.user.is_staff:
                return True
        return False


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return True
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    SAFE_METHODS = ["GET",]

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
