import base64

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from mainapp.models import Domain, Passwords, PasswordShare


User = get_user_model()


def decode(base64_string):

    base64_bytes = base64_string.encode("ascii")

    password_bytes = base64.b64decode(base64_bytes)
    password = password_bytes.decode("ascii")

    return password


class AccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class DomainSerializer(ModelSerializer):
    class Meta:
        model = Domain
        fields = "__all__"


class PasswordSerializer(ModelSerializer):
    user_password = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Passwords
        fields = "__all__"

    def get_user_password(self, instance):
        return decode(instance.user_password)


class PasswordShareSerializer(ModelSerializer):

    class Meta:
        model = PasswordShare
        fields = "__all__"
