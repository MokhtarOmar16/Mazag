from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreatePasswordRetypeSerializer as BaseUserCreateSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']
    def validate_username(self, value):
        if value.isdigit():
            raise serializers.ValidationError("Username cannot be entirely numeric.")
        return value

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']