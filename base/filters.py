import django_filters
from .models import Task
from django_filters import CharFilter

class TaskFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='startswith', max_length=10)
    class Meta:
        model = Task
        fields = ['title', 'complete']
