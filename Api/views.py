from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from .models import Cart, Category, MenuItem, Order, OrderItem
from .serializers import CartItemSerializer, MenuItemSerializer, UserSerializer

#
# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def menu_items(request):
#     if request.method == "GET":
#         items = MenuItem.objects.all()
#         serializer_items = MenuItemSerializer(items, many=True)
#         return Response(serializer_items.data)
#     if request.method == "POST":
#         manager = request.user.groups.filter(name="managers").exists()
#         if manager:
#             serializer_items = MenuItemSerializer(data=request.data)
#             serializer_items.is_valid(raise_exception=True)
#             serializer_items.save()
#             return Response(serializer_items.data, status.HTTP_201_CREATED)
#         return Response(
#             {"message": "You are not authorized"}, status.HTTP_403_FORBIDDEN


class MenuItemView(viewsets.ViewSet):
    permission_classes = IsAuthenticatedOrReadOnly

    def list(self, request):
        items = MenuItem.objects.all()
        serializer_items = MenuItemSerializer(items, many=True)
        return Response(serializer_items.data)

    def create(self, request):
        # permission_classes(ManagerPermission)
        serializer_items = MenuItemSerializer(data=request.data)
        serializer_items.is_valid(raise_exception=True)
        serializer_items.save()
        return Response(serializer_items.data, status.HTTP_201_CREATED)


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def delete(self, request, pk):
        manager = request.user.groups.filter(name="managers").exists()
        if not manager:
            return Response({"message": "unauthorized"}, status.HTTP_403_FORBIDDEN)
        item = get_object_or_404(MenuItem, id=pk)
        item.delete()
        return Response(
            {"message": "Deleted Successfully"},
        )

    def put(self, request, pk):
        manager = request.user.groups.filter(name="managers").exists()
        if not manager:
            return Response({"message": "unauthorized"}, status.HTTP_403_FORBIDDEN)
        item = get_object_or_404(MenuItem, id=pk)
        serializer_items = MenuItemSerializer(item, data=request.data)
        serializer_items.is_valid(raise_exception=True)
        serializer_items.save()
        return Response({"message": "Updated Successfully"})


class ManagerPermission(BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        user = request.user
        # managers = user.groups.filter(group__name="managers")
        # managers = User.objects.all().filter(groups__name="manager")
        # managers = Group.objects.all().filter(name="managers")
        if user and user.groups.filter(name="managers").exists():
            return True

        return False


class UserManagerView(viewsets.ViewSet):
    permission_classes = [ManagerPermission]
    # permission_classes(ManagerPermission)

    def list(self, request):
        users = User.objects.filter(groups__name="managers")
        items = UserSerializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        name = request.data["Username"]
        user = get_object_or_404(User, username=name)
        group = User.objects.filter(groups__name="managers")
        if user in group:
            return Response({"Message": "User already in group"})
        managers = Group.objects.get(name="managers")
        managers.user_set.add(user)
        return Response({"Message": "User added to manager group"}, status.HTTP_200_OK)

    def destroy(self, request):
        user = get_object_or_404(User, username=request.data["Username"])

        group = User.objects.filter(groups__name="managers")
        if user not in group:
            return Response({"Message": "Already removed"})
        managers = Group.objects.get(name="managers")
        managers.user_set.remove(user)
        return Response(
            {"Message": "User removed from manager group"}, status.HTTP_200_OK
        )


class UserDeliveryView(viewsets.ViewSet):
    permission_classes = [ManagerPermission]
    # permission_classes(ManagerPermission)

    def list(self, request):
        users = User.objects.filter(groups__name="delivery-crew")
        items = UserSerializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        name = request.data["Username"]
        user = get_object_or_404(User, username=name)
        # account = request.user.groups.filter(name="managers")
        # group = Group.objects.get(name="managers")
        group = User.objects.filter(groups__name="delivery-crew")
        if user in group:
            return Response({"Message": "User already in group"})
        managers = Group.objects.get(name="delivery-crew")
        managers.user_set.add(user)
        return Response({"Message": "User added to delivery crew"}, status.HTTP_200_OK)

    def destroy(self, request):
        user = get_object_or_404(User, username=request.data["Username"])

        group = User.objects.filter(groups__name="delivery-crew")
        if user not in group:
            return Response({"Message": "Already removed"})
        managers = Group.objects.get(name="delivery-crew")
        managers.user_set.remove(user)
        return Response(
            {"Message": "User removed from delivery crew"}, status.HTTP_200_OK
        )
