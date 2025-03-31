from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import user_list, verify_email, export_users_excel, register
from .views.api import RegisterAPIView, VerifyEmailAPIView, UserProfileAPIView

urlpatterns = [
    # Web URLs
    path('list/', user_list, name='user_list'),
    path('register/', register, name='register'),
    path('verify-email/<int:user_id>/', verify_email, name='verify_email'),
    path('export-excel/', export_users_excel, name='export_users_excel'),
    
    # API URLs
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/verify-email/', VerifyEmailAPIView.as_view(), name='api_verify_email'),
    path('api/profile/', UserProfileAPIView.as_view(), name='api_profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]