from django.db import transaction
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError

import base64

from mainapp.models import UserAccount, Domain, Passwords, PasswordShare
from mainapp.serializers import AccountSerializer, PasswordSerializer, DomainSerializer, PasswordShareSerializer


def encode(password):

    password_bytes = password.encode("ascii")

    base64_bytes = base64.b64encode(password_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


def decode(base64_string):

    base64_bytes = base64_string.encode("ascii")

    password_bytes = base64.b64decode(base64_bytes)
    password = password_bytes.decode("ascii")

    return password


class AccountViewSet(viewsets.ModelViewSet):
    """
    This api is used to do account CRUD operations
    """

    queryset = UserAccount.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer


class PasswordViewSet(viewsets.ModelViewSet):
    """
    This api is used to do user passwords CRUD operations
    """

    queryset = Passwords.objects.all()
    serializer_class = PasswordSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        password = encode(self.request.data.get("user_password"))
        serializer.save(created_by=user, user_password=password)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id not in [instance.created_by.id] + list(UserAccount.objects.filter(
                passwordshare__password=instance, passwordshare__access_type="E").values_list("id", flat=True)):
            raise ValidationError("Access denied.")
        request.data["password"] = encode(request.data.get("password"))
        return super(PasswordViewSet, self).update(request, *args, **kwargs)


class PasswordShareViewSet(viewsets.ModelViewSet):
    """
    This api is used to do item share CRUD operations
    """

    queryset = PasswordShare.objects.all()
    serializer_class = PasswordShareSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        password = request.data.get("passwords")
        password = Passwords.objects.get(id=password)
        if request.user.id not in [password.created_by.id] + list(UserAccount.objects.filter(
                passwordshare__passwords=password, passwordshare__access_type="E").values_list("id", flat=True)):
            raise ValidationError("Access denied.")

        return super(PasswordShareViewSet, self).create(request, *args, **kwargs)

