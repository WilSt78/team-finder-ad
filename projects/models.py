from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from .constants import (
    MAX_LENGTH_NAME,
    STATUS_CHOICES,
    MAX_LENGTH_STATUS,
    STATUS_OPEN,
)
from .validators import github_validator

User = get_user_model()


class Project(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME, verbose_name="название"
    )
    description = models.TextField(null=True, verbose_name="описание")
    owner = models.ForeignKey(
        to=User,
        related_name="owned_projects",
        on_delete=models.CASCADE,
        verbose_name="автор",
    )
    created_at = models.DateTimeField(
        default=timezone.now, null=False, verbose_name="дата создания"
    )
    github_url = models.URLField(
        null=True,
        validators=[github_validator],
        verbose_name="ссылка на Github",
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
        max_length=MAX_LENGTH_STATUS,
        verbose_name="статус проекта",
    )
    participants = models.ManyToManyField(
        User,
        through="Participants",
        related_name="participated_projects",
        verbose_name="участники",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "проект"
        verbose_name_plural = "проекты"


class Participants(models.Model):
    user = models.ForeignKey(
        to=User,
        null=True,
        on_delete=models.CASCADE,
        related_name="participations",
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="participant_entries",
    )

    def __str__(self):
        return f"{self.user.name} - {self.project.name}"

    class Meta:
        verbose_name = "участник"
        verbose_name_plural = "участники"
