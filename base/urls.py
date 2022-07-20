from django.urls import path
from .views import IndexView, TaskDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('task/<int:pk>', TaskDetailView.as_view(), name='task')
]
