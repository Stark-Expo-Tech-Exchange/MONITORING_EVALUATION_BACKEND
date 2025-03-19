from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .models import Project, Indicator, Report
from .serializers import ProjectSerializer, IndicatorSerializer, ReportSerializer, UserRegistrationSerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import PasswordResetSerializer

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
 
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

User = get_user_model()  # This will get the user model (default or custom)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


# User Registration

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()


# Admin Authentication
class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({"message": "Hello, Admin!"})


# User Profile API
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

        # Check if the User model has a 'role' field
        if hasattr(user, 'role'):
            data["role"] = user.role

        return Response(data)

#passwordresed

# @method_decorator(csrf_exempt, name='dispatch')

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "No user with this email exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate token and uid
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://localhost:8000/api/password_reset_confirm/{uid}/{token}/"

        # Send the email
        send_mail(
            subject='Password Reset Request',
            message=f'You can reset your password using this link: {reset_link}',
            from_email='sparkwilson2041@gmail.com',
            recipient_list=[email],
        )

        return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)

#to confirm password
@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Set the new password
            user.set_password(request.data['password'])
            user.save()
            return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
