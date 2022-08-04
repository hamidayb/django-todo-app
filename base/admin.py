from django.contrib import admin
from .models import Task, User
from django.contrib.auth.admin import UserAdmin
# Register your models here.



@admin.register(Task)
class TaskView(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'description',
                    'complete', 'created', 'updated']

class UserAdminView(admin.ModelAdmin):
    list_display = ['id', 'email', 'name', 'age', 'city', 'country', 'created', 'password']


# admin.site.register(Task, TaskView)
admin.site.register(User, UserAdminView)
