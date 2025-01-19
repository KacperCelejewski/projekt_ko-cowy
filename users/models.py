# users/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Zmieniamy related_name, aby uniknąć konfliktu
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Zmieniamy related_name, aby uniknąć konfliktu
        blank=True,
    )
