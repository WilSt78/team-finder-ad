from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from projects.validators import github_validator

from .constants import *
from .utils import generate_avatar
from .validators import validate_phone_format, validate_unique_phone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Skill(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_SKILLS_NAME)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=MAX_LENGTH_USER_NAME)
    surname = models.CharField(max_length=MAX_LENGTH_SURNAME)
    avatar = models.ImageField(null=False, upload_to="avatars/")
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        validators=[validate_phone_format, validate_unique_phone],
    )
    github_url = models.URLField(
        null=True, validators=[github_validator]
    )
    about = models.TextField(max_length=MAX_LENGTH_ABOUT)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    skills = models.ManyToManyField(
        Skill, through="UserSkills", related_name="acquired_skills"
    )

    USERNAME_FIELD = "email"
    objects = UserManager()

    def save(self, *args, **kwargs):
        is_new = not self.pk

        if is_new and not self.avatar:
            super().save(*args, **kwargs)
            img = generate_avatar(self)
            super().save(update_fields=["avatar"])
        else:
            super().save(*args, **kwargs)


class UserSkills(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    skill = models.ForeignKey(
        to=Skill,
        on_delete=models.CASCADE,
        related_name="user_skills",
        null=True,
    )
