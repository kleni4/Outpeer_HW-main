from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random

from ..serializers import UserSerializer, UserRegistrationSerializer

User = get_user_model()

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)
            
            # Генерация кода подтверждения
            verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            user.verification_code = verification_code
            user.verification_code_created_at = timezone.now()
            user.save()
            
            # Отправка кода на email
            send_mail(
                'Подтверждение регистрации',
                f'Ваш код подтверждения: {verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            return Response({
                'message': 'Пользователь успешно зарегистрирован. Проверьте email для подтверждения.',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get('user_id')
        verification_code = request.data.get('verification_code')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, 
                          status=status.HTTP_404_NOT_FOUND)

        if (user.verification_code == verification_code and 
            user.verification_code_created_at + timedelta(minutes=30) > timezone.now()):
            user.is_active = True
            user.is_email_verified = True
            user.verification_code = None
            user.verification_code_created_at = None
            user.save()

            # Создаем токены
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Email успешно подтвержден',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Неверный код или код устарел'
        }, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
