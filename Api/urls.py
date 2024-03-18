from django.urls import path

from . import views

urlpatterns = [
    path("menu-items/<int:pk>/", views.SingleMenuItemView.as_view()),
    path("menu-items/", views.menu_items),
    # path("cart/menu-items/", views.CartItemView.as_view()),
    # path("groups/manager/users/", views.UserView.as_view()),
    # path("groups/managers/users/", views.user_view),
    path(
        "groups/manager/users",
        views.UserView.as_view({"get": "list"}),
    ),
]
