from django import forms

from .models import Project
from .constants import *


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status',)
        widgets = {
            "status": forms.Select(choices=STATUS_CHOICES)
        }
