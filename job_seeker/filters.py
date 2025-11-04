from django_filters.rest_framework import FilterSet
from employer.models import Job


class ProductFilter(FilterSet):
    class Meta:
        model = Job
        fields = {
            'category_id': ['exact'],
                            }