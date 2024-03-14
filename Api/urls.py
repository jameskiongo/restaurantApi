from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("menu-items/<int:pk>", views.single_item),
    path("menu-items", views.menu_items),
]
