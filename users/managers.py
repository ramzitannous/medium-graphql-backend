from typing import TYPE_CHECKING, Optional

from django.contrib.auth.models import BaseUserManager
from django.db.models.manager import Manager

if TYPE_CHECKING:
    from users.models import Following, User


class UsersManager(BaseUserManager):
    def create_user(
        self, email: str, password: Optional[str] = None, **extra_fields
    ) -> "User":
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email: str, password: Optional[str] = None, **extra_fields
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is False:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class FollowingManager(Manager):
    def follow(self, user: "User", another_user: "User") -> "Following":
        """user a follows user b"""
        follow = self.model()
        follow.follower = user
        follow.followed = another_user
        follow.save()
        return follow

    def unfollow(self, user: "User", another_user: "User") -> bool:
        """user a  unfollows user b"""
        try:
            follow = self.get(follower=user, followed=another_user)
            follow.delete()
            return True
        except Following.DoesNotExist:
            return False

    def is_following(self, user: "User", profile: "User") -> bool:
        return self.filter(follower=user, followed=profile).exists()
