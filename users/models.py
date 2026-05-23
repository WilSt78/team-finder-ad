from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models

from projects.validators import github_validator

from .managers import UserManager
from .constants import (
    MAX_LENGTH_SKILLS_NAME,
    MAX_LENGTH_ABOUT,
    MAX_LENGTH_PHONE,
    MAX_LENGTH_SURNAME,
    MAX_LENGTH_USER_NAME,
)
from .user_utils import generate_avatar
from .validators import validate_phone_format, validate_unique_phone


class Skill(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_SKILLS_NAME, verbose_name="название"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "навык"
        verbose_name_plural = "навыки"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="почта")
    name = models.CharField(
        max_length=MAX_LENGTH_USER_NAME, verbose_name="имя"
    )
    surname = models.CharField(
        max_length=MAX_LENGTH_SURNAME, verbose_name="фамилия"
    )
    avatar = models.ImageField(
        null=False, upload_to="avatars/", verbose_name="аватарка"
    )
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        validators=[validate_phone_format, validate_unique_phone],
        verbose_name="телефон",
    )
    github_url = models.URLField(
        null=True,
        validators=[github_validator],
        verbose_name="ссылка на Github",
    )
    about = models.TextField(
        max_length=MAX_LENGTH_ABOUT, verbose_name="описание профиля"
    )
    is_active = models.BooleanField(
        default=True, verbose_name="активный пользователь"
    )
    is_staff = models.BooleanField(
        default=False, verbose_name="администратор"
    )
    skills = models.ManyToManyField(
        Skill,
        through="UserSkills",
        related_name="acquired_skills",
        verbose_name="навыки",
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class UserSkills(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="skills_user"
    )
    skill = models.ForeignKey(
        to=Skill,
        on_delete=models.CASCADE,
        related_name="user_skills",
        null=True,
    )

    class Meta:
        verbose_name = "навык пользователя"
        verbose_name_plural = "навыки пользователей"
