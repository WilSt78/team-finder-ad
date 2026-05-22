from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from .utils import generate_avatar
from .constants import *
from .validators import validate_phone_format, validate_unique_phone    
from projects.validators import github_validator


class Skill(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_SKILLS_NAME
    )

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True
    )
    name = models.CharField(
        max_length = MAX_LENGTH_USER_NAME
    )
    surname = models.CharField(
        max_length = MAX_LENGTH_SURNAME
    )
    avatar = models.ImageField(
        null = False,
        upload_to='avatars/'
    )
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        validators=[validate_phone_format, validate_unique_phone]
    )
    github_url = models.URLField(
        null = True,
        validators=[github_validator]
    )
    about = models.TextField(
        max_length=MAX_LENGTH_ABOUT
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff =  models.BooleanField(
        default=False
    )
    skills = models.ForeignKey(
        to=Skill,
        related_name='users',
        null= True,
        on_delete = models.CASCADE
    )

    USERNAME_FIELD = 'email'
    objects = BaseUserManager()

    
    def save(self, *args, **kwargs):
        is_new = not self.pk
        
        if is_new and not self.avatar:
            super().save(*args, **kwargs)
            img = generate_avatar(self)
            super().save(update_fields=['avatar'])
        else:
            super().save(*args, **kwargs)

