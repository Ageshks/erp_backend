import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    email = request.data.get('email', '').strip().lower()
    password = request.data.get('password', '')
    full_name = request.data.get('full_name', '').strip()

    if not email or not password or not full_name:
        return Response({'detail': 'Email, password, and full name are required.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({'detail': 'A user with that email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    name_parts = full_name.split(maxsplit=1)
    user = User.objects.create_user(email=email, password=password)
    user.first_name = name_parts[0]
    user.last_name = name_parts[1] if len(name_parts) > 1 else ''
    user.save(update_fields=['first_name', 'last_name'])

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'redirect_url': '/',
            'user': {'email': user.email, 'full_name': user.get_full_name()},
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email', '').strip().lower()
    password = request.data.get('password', '')

    if not email or not password:
        return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()
    if user is None or not user.check_password(password):
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'redirect_url': '/',
            'user': {'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name},
        },
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_view(request):
    email = request.data.get('email', '').strip().lower()
    if not email:
        return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()
    if user is None:
        return Response({'detail': 'This email is not registered.'}, status=status.HTTP_404_NOT_FOUND)

    token = secrets.token_urlsafe(24)
    user.reset_token = token
    user.save(update_fields=['reset_token'])
    send_mail(
        'Password reset request',
        f'Use this token to reset your password: {token}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=True,
    )

    return Response({'detail': 'A reset token has been sent to your email.', 'reset_token': token}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_view(request):
    email = request.data.get('email', '').strip().lower()
    token = request.data.get('token', '')
    new_password = request.data.get('new_password', '')

    if not email or not token or not new_password:
        return Response({'detail': 'Email, token, and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()
    if user is None or getattr(user, 'reset_token', None) != token:
        return Response({'detail': 'Invalid or expired reset token.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.reset_token = None
    user.save(update_fields=['password', 'reset_token'])
    return Response({'detail': 'Password reset successful.', 'redirect_url': '/'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data_view(request):
    user = request.user
    return Response(
        {
            'message': 'Authenticated dashboard data',
            'redirect_url': '/',
            'user': {'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name},
        },
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except TokenError:
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
