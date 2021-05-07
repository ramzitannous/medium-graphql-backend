from core.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from users.managers import FollowingManager, UsersManager


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UsersManager()

    username = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=200, unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="images", editable=True, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


class Following(BaseModel):
    followed = models.ForeignKey(
        User, related_name="followed_set", on_delete=models.CASCADE
    )
    follower = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (
            "followed",
            "follower",
        )

    objects = FollowingManager()
