from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Cart, Category, MenuItem, Order, OrderItem


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
    # menu_item = MenuItemSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=serializers.CurrentUserDefault
    )

    # user_id = serializers.IntegerField(write_only=True)
    def validate(self, attrs):
        attrs["price"] = attrs["quantity"] * attrs["unit_price"]
        return attrs

    class Meta:
        model = Cart
        fields = [
            "user",
            "menuitem",
            "quantity",
            "unit_price",
            "price",
        ]

    def calculate_price(self, unit_price, quantity):
        return unit_price * quantity
