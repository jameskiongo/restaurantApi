from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, Category, MenuItem, Order, OrderItem
from .serializers import MenuItemSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def menu_items(request):
    if request.method == "GET":
        items = MenuItem.objects.select_related("category").all()
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)
    elif request.method == "POST":
        serialized_items = MenuItemSerializer(data=request.data)
        serialized_items.is_valid(raise_exception=True)
        serialized_items.save()
        return Response(serialized_items.data, status.HTTP_201_CREATED)


@api_view()
def single_item(request):
    return Response({"message": "single item"})
