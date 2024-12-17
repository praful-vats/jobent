from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import UserProfile
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import status

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=401)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        return Response({
            "username": request.user.username,
            "user_type": profile.user_type,
            "premium_tokens": profile.premium_tokens,
        })


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)
        user = User.objects.create_user(username=username, password=password)
        # Ensure UserProfile is created only if it doesn't exist
        UserProfile.objects.get_or_create(user=user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)