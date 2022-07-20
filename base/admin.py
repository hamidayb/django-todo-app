from django.contrib import admin
from .models import Task
# Register your models here.


class TaskView(admin.ModelAdmin):
    list_display = ['title', 'description', 'complete', 'created']


admin.site.register(Task, TaskView)
