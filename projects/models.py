from django.db import models
from django.utils import timezone

from .validators import github_validator
from users.models import User
from .constants import *

class Project(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME
    )
    description = models.TextField(
        null = True
    )
    owner = models.ForeignKey(
        to = User,
        related_name = "owned_projects",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        null=False
    )
    github_url = models.URLField(
        null = True,
        validators=[github_validator]
    )
    status = models.CharField(
        null=False,
        choices=STATUS_CHOICES,
        max_length=MAX_LENGTH_STATUS
    )
    participants = models.ManyToManyField(
        User,
        through='Participants',
        related_name="participated_projects"
    )
    
class Participants(models.Model):
    user = models.ForeignKey(
        to = User,
        null = True,
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        to = Project,
        on_delete=models.CASCADE,
        related_name='participant_entries'
    )