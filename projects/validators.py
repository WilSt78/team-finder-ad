import re

from django.core.exceptions import ValidationError

def github_validator(url):
    GITHUB_REGEX = r'^https?:\/\/(www\.)?github\.com\/[\w\-\.]+(\/[\w\-\.]+)?\/?$'

    if not url:
        return url
    if not re.match(GITHUB_REGEX, url):
        raise ValidationError("Требуется валидная ссылка на Github")