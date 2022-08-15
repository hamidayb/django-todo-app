from asyncio import tasks
from django.urls import path
from .views import IndexView, TaskChangeAPI, TaskDetailView, TaskCreateView, TaskEdit, TaskEditUsingMixin, TaskListAPI, TaskListUsingMixin, TaskUpdateView, TaskDeleteView, CustomLoginView, CustomRegisterView, TaskChangeAPI, TasksView, TimeView, api_overview
from django.contrib.auth.views import LogoutView

# from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'base'

urlpatterns = [
    path('times/', TimeView.as_view(), name='times'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('register', CustomRegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(next_page='base:login'), name='logout'),
    path('', IndexView.as_view(), name='index'),
    path('task/<int:pk>', TaskDetailView.as_view(), name='task'),
    path('task-create',
         TaskCreateView.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdateView.as_view(), name='task-update'),
    path('task-delete/<int:pk>', TaskDeleteView.as_view(), name='task-delete'),


    path('api/', api_overview, name="api_overview"),
    path('api/tasks', TaskListAPI.as_view(), name="tasks"),
    path('api/task/<int:pk>', TaskChangeAPI.as_view(), name="task-change"),

    path('api/task-list', TaskListUsingMixin.as_view(), name="task-list"),
    path('api/task-edit/<int:pk>', TaskEditUsingMixin.as_view(), name="task-edit"),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
