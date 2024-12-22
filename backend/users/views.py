from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from .models import UserProfile
from .serializers import UserProfileSerializer

# Signup View
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            # Extracting user data
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')
            password = data.get('password')

            if not first_name or not last_name or not email or not password:
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user already exists
            if User.objects.filter(username=email).exists():
                return Response({'error': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)

            # Create new user
            user = User.objects.create_user(
                username=email, first_name=first_name, last_name=last_name, email=email, password=password
            )

            # Check if UserProfile already exists for the user
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            # Set initial tokens and premium status if the profile is newly created
            if created:
                user_profile.tokens = 100  # Assign 100 tokens by default
                user_profile.is_premium = False  # Set user to normal initially
                user_profile.save()
            
            # Generate token
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(username=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Endpoint to add more tokens (e.g., when a user buys more credits)
class AddTokensView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            try:
                # Fetch user profile
                profile = UserProfile.objects.get(user=user)

                # Add tokens (for example, adding 200 tokens)
                profile.tokens += 200  # You can modify the amount as per your logic
                profile.is_premium = True  # Promote to premium user
                profile.save()

                return Response({'message': 'Tokens added successfully, and you are now a premium user!'}, status=status.HTTP_200_OK)

            except UserProfile.DoesNotExist:
                return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)


# View to check user profile details
class UserProfileView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                serializer = UserProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except UserProfile.DoesNotExist:
                return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
