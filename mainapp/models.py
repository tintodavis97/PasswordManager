from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserAccount(AbstractUser):
    pass


class Domain(models.Model):
    domain_name = models.CharField(max_length=128)
    domain_link = models.CharField(max_length=256)


class Passwords(models.Model):
    """
    This model is used to store user items.
    """

    created_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE, editable=False, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    description = models.TextField(null=True, blank=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=128)
    user_password = models.CharField(max_length=256)


class PasswordShare(models.Model):
    """
    This model is used to store shared item and user.
    """

    ACCESS_TYPE = (("V", "VIEW"), ("E", "EDIT"))
    passwords = models.ForeignKey(Passwords, on_delete=models.CASCADE)
    shared_to = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    access_type = models.CharField(max_length=4, choices=ACCESS_TYPE, default="V")
