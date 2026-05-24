import hashlib
import random
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from .constants import (
    AVATAR_FONT_NAME,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
    X_ANCHOR,
    Y_ANCHOR,
)


def get_first_letter(user):
    return user.name[0].upper() if user.name else "?"


def generate_avatar(user):
    size = AVATAR_SIZE
    letter = get_first_letter(user)
    bg_color = tuple(random.randint(50, 200) for _ in range(3))

    image = Image.new("RGB", (size, size), color=bg_color)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(AVATAR_FONT_NAME, AVATAR_FONT_SIZE)
    except:
        font = ImageFont.load_default(size=AVATAR_FONT_SIZE)

    bbox = draw.textbbox((X_ANCHOR, Y_ANCHOR), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = (
        (size - text_width) // 2,
        (size - text_height) // 2,
    )
    draw.text(position, letter, fill=AVATAR_TEXT_COLOR, font=font)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    filename = f"avatar_{user.email}_{
        hashlib.md5(str(random.random()).encode()).hexdigest()[:8]
    }.png"
    user.avatar.save(filename, ContentFile(buffer.read()), save=False)
    buffer.close()

    return user.avatar
