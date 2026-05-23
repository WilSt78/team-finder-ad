import hashlib
import random
from io import BytesIO

from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import JsonResponse
from PIL import Image, ImageDraw, ImageFont

from .constants import *


def get_first_letter(user):
    return user.name[0].upper() if user.name else "?"


def generate_avatar(user):
    size = AVATAR_SIZE
    letter = get_first_letter(user)
    bg_color = (
        random.randint(50, 200),
        random.randint(50, 200),
        random.randint(50, 200),
    )

    image = Image.new("RGB", (size, size), color=bg_color)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(AVATAR_FONT_NAME, AVATAR_FONT_SIZE)
    except:
        font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        position = (
            (size - text_width) // 2,
            (size - text_height) // 2,
        )
        draw.text(position, letter, fill="white", font=font)

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        filename = f"avatar_{user.email}_{hashlib.md5(str(random.random()).
            encode()).hexdigest()[:8]}.png"
        user.avatar.save(
            filename, ContentFile(buffer.read()), save=False
        )
        buffer.close()

    return user.avatar


def search_skills(request):
    from .models import Skill

    query = request.GET.get("q", "").strip()
    skills_queryset = Skill.objects.filter(
        Q(name__istartswith=query)
    ).order_by("name")[:SKILL_QUERY_SIZE]
    skills_data = [
        {"id": skill.id, "name": skill.name}
        for skill in skills_queryset
    ]
    return JsonResponse(skills_data, safe=False)
