"""
===========================================
apps/jobs/filters.py
===========================================
"""

import django_filters
from .models import Job


class JobFilter(django_filters.FilterSet):
    """Filter for job listings"""
    
    category = django_filters.UUIDFilter(field_name='category__id')
    location = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Job
        fields = ['category', 'location']

