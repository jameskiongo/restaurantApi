# from auth.custom_permissions import CustomerPermission, ManagerPermission
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets

# from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .custom_permissions import CustomerPermission, ManagerPermission
from .models import Cart, Category, MenuItem, Order, OrderItem
from .serializers import (
    CartItemSerializer,
    MenuItemSerializer,
    OrderItemSerializer,
    UserSerializer,
)

# from rest_framework.decorators import api_view


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


class CartItemView(viewsets.ViewSet):
    queryset = Cart.objects.all()
    permission_classes = [CustomerPermission]

    def list(self, request):
        user = self.request.user
        items = Cart.objects.filter(user=user)
        if items:
            serializer_items = CartItemSerializer(items, many=True)
            return Response(serializer_items.data)
        return Response({"Message": "Add Items to Cart"})

    def create(self, request, *args, **kwargs):
        item = request.data.get("Menu Item")
        menuitems = MenuItem.objects.filter(title=item)
        if not menuitems.exists():
            return Response({"Message": "Item not in Menu"}, status.HTTP_404_NOT_FOUND)
            # choose_item = get_object_or_404(Cart, menuitem__title=item)
            # choose_item = Cart.objects.get(menuitem__title=item)
            # user = self.request.user
            # user.user_set.add(choose_item)
            # user.add(choose_item)
            # serializer_items = CartItemSerializer(choose_item)
            # serializer_items.is_valid(raise_exception=True)
            # serializer_items.save()
            # return Response("Ok")
        # return Response({"Message": "Item not in Menu"}, status.HTTP_404_NOT_FOUND)
        serializer_items = CartItemSerializer(data=request.data)
        serializer_items.is_valid(raise_exception=True)
        serializer_items.save(menuitems=menuitems)
        return Response(serializer_items.data, status.HTTP_201_CREATED)

    def destroy(self, request):
        user = self.request.user
        items = Cart.objects.filter(user=user)
        if items:
            items.delete()
            return Response({"Message": "Deleted All Successfully"}, status.HTTP_200_OK)
        return Response({"Message": "Add Items to Cart"})


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


class OrderView(viewsets.ViewSet):
    permission_classes = [CustomerPermission]

    def list(self, request):
        user = self.request.user
        orders = Order.objects.filter(user=user)
        serializer_items = OrderItemSerializer(orders, many=True)
        return Response(serializer_items.data)
