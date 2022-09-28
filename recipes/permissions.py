from rest_framework import permissions


# Checando se o usuario é dono da recipe
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)
