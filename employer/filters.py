"""
===========================================
apps/jobs/filters.py
===========================================
"""

from django_filters.rest_framework import FilterSet
from .models import *

class JobCategoryFilter(FilterSet):
    class Meta:
        model = Job
        fields = {
            'category_id': ['exact'],
        }

