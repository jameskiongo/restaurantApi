from rest_framework.permissions import BasePermission

from .models import User


class ManagerPermission(BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        user = request.user
        if user and user.groups.filter(name="managers").exists():
            return True

        return False


class CustomerPermission(BasePermission):
    message = "You have to be a customer "

    def has_permission(self, request, view):
        user = request.user
        group1 = User.objects.filter(groups__name="managers")
        group2 = User.objects.filter(groups__name="delivery-crew")

        if user in (group1 or group2):
            return False
        return True
