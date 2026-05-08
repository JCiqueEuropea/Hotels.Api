from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsHotelManager(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "is_hotel_manager", False)
        )
    
class IsTheSameUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.pk == request.user.pk