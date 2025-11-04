"""
===========================================
utils/validators.py
===========================================
"""

from django.core.exceptions import ValidationError
from django.conf import settings
import os


def validate_file_size(file):
    """Validate file size"""
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(f'File size cannot exceed {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB')


def validate_resume_extension(file):
    """Validate resume file extension"""
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in settings.ALLOWED_RESUME_EXTENSIONS:
        raise ValidationError(
            f'Unsupported file extension. Allowed extensions: {", ".join(settings.ALLOWED_RESUME_EXTENSIONS)}'
        )



