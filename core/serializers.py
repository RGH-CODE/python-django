from core.models import User

from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer
)


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User

        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User

        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name'
        ]