# users/validators.py
import re

from django.core.exceptions import ValidationError


def normalize_phone(phone):
    if not phone:
        return phone
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 11 and digits.startswith("8"):
        return "+7" + digits[1:]
    elif len(digits) == 11 and digits.startswith("7"):
        return "+" + digits
    elif len(digits) == 10:
        return "+7" + digits
    return phone


def validate_phone_format(value):
    if not value:
        return value
    normalized = normalize_phone(value)
    if not re.match(r"^\+7\d{10}$", normalized):
        raise ValidationError(
            "Номер телефона должен быть в формате8XXXXXXXXXX или +7XXXXXXXXXX"
        )

    return normalized


def validate_unique_phone(value, instance=None):
    from .models import User

    if not value:
        return value
    normalized = normalize_phone(value)
    queryset = User.objects.filter(phone=normalized)
    if instance and instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    if queryset.exists():
        raise ValidationError(
            "Пользователь с таким номером телефона уже существует",
        )

    return normalized
