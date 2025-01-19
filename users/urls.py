# users/urls.py
from django.urls import path
from .views import RegisterView, UserDetailView, LoginView
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", UserDetailView.as_view(), name="profile"),
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
