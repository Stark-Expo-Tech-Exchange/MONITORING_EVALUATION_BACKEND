# monitoring/urls.py
from django.urls import path
from .views import UserRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserProfileView  # Ensure this is imported

from .views import PasswordResetView
from django.contrib.auth import views as auth_views #for email reset link

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IndicatorViewSet, ReportViewSet, UserRegistrationView, AdminOnlyView, UserProfileView

from .views import (
    UserRegistrationView, 
    UserProfileView, 
    ProjectViewSet, 
    IndicatorViewSet, 
    ReportViewSet
)

# Using DefaultRouter for ViewSets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'indicators', IndicatorViewSet)
router.register(r'reports', ReportViewSet)

# Merge all urlpatterns into one list
urlpatterns = [
    path('api/', include(router.urls)),  # Includes API endpoints for viewsets
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Password Reset URLs
    path('api/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('api/password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # User Profile URL
    path('api/profile/', UserProfileView.as_view(), name='profile'),
]
