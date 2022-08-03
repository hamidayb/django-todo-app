from django.contrib import admin
from .models import Task, User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class TaskView(admin.ModelAdmin):
    list_display = ['user', 'title', 'description',
                    'complete', 'created', 'updated']


class UserAdminView(admin.ModelAdmin):
    list_display = ['email', 'name', 'age', 'city', 'created']


admin.site.register(Task, TaskView)
admin.site.register(User, UserAdminView)
