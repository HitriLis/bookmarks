from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import viewsets, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    RegistrationSerializer,
    TokenResponseSerializer,
    TokenRefreshResponseSerializer
)


class RefreshTokenView(TokenRefreshView):
    @extend_schema(
        tags=['Auth'],
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        },
        description="Refresh token"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    @extend_schema(
        tags=['Auth'],
        responses={
            status.HTTP_200_OK: TokenResponseSerializer,
        },
        description="User login"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegistrationView(generics.GenericAPIView):
    """
    Register user.
    """
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=['Auth'],
        responses={
            status.HTTP_201_CREATED: TokenResponseSerializer,
        },
        description="User registration"
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        )
