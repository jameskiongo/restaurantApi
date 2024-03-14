from django.urls import path

from . import views

urlpatterns = [
    path("menu-items/<int:pk>/", views.SingleMenuItemView.as_view()),
    path("menu-items/", views.menu_items),
    path("cart/menu-items/", views.CartItemView.as_view()),
]
