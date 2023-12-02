from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()


class TokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.register(
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
