from django import forms

from .constants import STATUS_CHOICES
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "name",
            "description",
            "github_url",
            "status",
        )
        widgets = {"status": forms.Select(choices=STATUS_CHOICES)}
