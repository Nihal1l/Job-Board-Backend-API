"""
===========================================
utils/helpers.py
===========================================
"""

from django.utils.text import slugify
import random
import string


def generate_unique_slug(model_class, title):
    """Generate unique slug for a model"""
    slug = slugify(title)
    unique_slug = slug
    counter = 1
    
    while model_class.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
    
    return unique_slug


def generate_random_string(length=32):
    """Generate random string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
