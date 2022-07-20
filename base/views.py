from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task


class IndexView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/index.html'


class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'