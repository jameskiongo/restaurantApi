from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Cart, Category, MenuItem, Order, OrderItem
from .serializers import CartItemSerializer, MenuItemSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def menu_items(request):
    if request.method == "GET":
        items = MenuItem.objects.all()
        serializer_items = MenuItemSerializer(items, many=True)
        return Response(serializer_items.data)
    if request.method == "POST":
        # manager = Group.objects.get(name="managers")
        manager = request.user.groups.filter(name="managers").exists()
        if manager:
            serializer_items = MenuItemSerializer(data=request.data)
            serializer_items.is_valid(raise_exception=True)
            serializer_items.save()
            return Response(serializer_items.data, status.HTTP_201_CREATED)
        return Response(
            {"message": "You are not authorized"}, status.HTTP_403_FORBIDDEN
        )


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
            return Response({"message": "forbidden"}, status.HTTP_403_FORBIDDEN)
        item = get_object_or_404(MenuItem, id=pk)
        item.delete()
        return Response(
            {"message": "Deleted Successfully"},
        )

    def put(self, request, pk):
        manager = request.user.groups.filter(name="managers").exists()
        if not manager:
            return Response({"message": "forbidden"}, status.HTTP_403_FORBIDDEN)
        item = get_object_or_404(MenuItem, id=pk)
        serializer_items = MenuItemSerializer(item, data=request.data)
        serializer_items.is_valid(raise_exception=True)
        serializer_items.save()
        return Response({"message": "Updated Successfully"})


class CartItemView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)
