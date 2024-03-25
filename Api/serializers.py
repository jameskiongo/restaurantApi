from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Cart, Category, MenuItem, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "title"]


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ["title", "price", "featured", "category", "category_id"]


class CartItemSerializer(serializers.ModelSerializer):
    # menuitem = MenuItemSerializer(read_only=True, many=True)
    menuitem = serializers.CharField(read_only=True)
    user = UserSerializer(
        many=False, read_only=True, default=serializers.CurrentUserDefault()
    )
    # price = serializers.SerializerMethodField(method_name="calculate_price")

    class Meta:
        model = Cart
        fields = ["user", "menuitem", "quantity", "price"]
        extra_kwargs = {
            "quantity": {"min_value": 1},
        }

    def calculate_price(self, price, quantity: Cart):
        return price * quantity.menuitem


class OrderItemSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        many=False, read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Order
        fields = ["user", "delivery_crew", "status", "total", "date"]
