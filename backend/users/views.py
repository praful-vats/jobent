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
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get user by email
            user = User.objects.get(email=email)
            print(f"User found: {user.username}")

            # Authenticate using the username field
            authenticated_user = authenticate(request, username=user.username, password=password)
            
            if authenticated_user:
                print("User authenticated successfully")
                token, _ = Token.objects.get_or_create(user=authenticated_user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                print("Authentication failed")

        except User.DoesNotExist:
            print("User not found")

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

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
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('firstName')
        last_name = request.data.get('lastName')
        birthday = request.data.get('birthday')

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.birthday = birthday
        profile.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)