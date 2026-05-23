from django import forms
from django.contrib.auth import authenticate

from .constants import *
from .models import User


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "surname", "email", "password")


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError(
                    "Неверный email или пароль"
                )
            self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, "user", None)


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "name",
            "surname",
            "avatar",
            "about",
            "phone",
            "github_url",
        )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise forms.ValidationError("Новые пароли не совпадают")
        return cleaned_data
