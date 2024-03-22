from django.urls import path

from . import views

urlpatterns = [
    path("menu-items/<int:pk>/", views.SingleMenuItemView.as_view()),
    path(
        "cart/menu-items/",
        views.CartItemView.as_view(
            {
                "get": "list",
                "post": "create",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "menu-items/",
        views.MenuItemView.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "groups/manager/users",
        views.UserManagerView.as_view(
            {
                "get": "list",
                "post": "create",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "groups/delivery-crew/users",
        views.UserDeliveryView.as_view(
            {
                "get": "list",
                "post": "create",
                "delete": "destroy",
            }
        ),
    ),
]
