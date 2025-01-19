# users/views.py
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Widok rejestracji użytkownika
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer


# Widok pobierania informacji o użytkowniku
class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Zwróci bieżącego zalogowanego użytkownika


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)

            if user is not None:
                # Generowanie tokenów JWT
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Tworzymy nowego użytkownika
            login(request, user)  # Logujemy użytkownika
            return redirect(
                "home"
            )  # Przekierowujemy na stronę główną (lub inną stronę po rejestracji)
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})
