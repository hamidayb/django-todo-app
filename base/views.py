from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime
import time

from django.contrib.auth import login, authenticate
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status

from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import UserRegistrationForm
from .filters import TaskFilter
from .models import Task, Time
from .serializers import TaskSerializer


class TimeView(ListView):
    model = Time
    fields = "__all__"
    context_object_name = 'times_list'
    template_name = 'base/times.html'



@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Add Task / Display all Tasks': 'api/tasks',
        'Task Detail/Update/Delete': 'api/task/<int:pk>',
        '(Using Mixin) Add Task / Display all Tasks': 'api/task-list',
        '(Using Mixin) Task Detail / Update / Delete': 'api/task-edit/<int:pk>',
    }
    dt = datetime.utcnow()

    return Response(time.tzname)


class TaskListAPI(APIView):

    def get(self, request):
        tasks = Task.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskChangeAPI(APIView):

    def get_object(self, pk):
        try:
            return Task.tasks.get(id=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response('Task Deleted')


class TaskListUsingMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Task.tasks.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskEditUsingMixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Task.tasks.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TasksView(generics.ListCreateAPIView):
    queryset = Task.tasks.all()
    serializer_class = TaskSerializer


class TaskEdit(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.tasks.all()
    serializer_class = TaskSerializer


class CustomLoginView(LoginView):
    fields = '__all__'
    template_name = 'base/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('base:index')


class CustomRegisterView(FormView):
    template_name = 'base/register.html'
    form_class = UserRegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('base:index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            authenticate(email=email, password=raw_password)
            login(self.request, user)
        return super(CustomRegisterView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('base:index',  *args, **kwargs)
        return super(CustomRegisterView, self).get(request, *args, **kwargs)


class IndexView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = context['tasks'].filter(user=self.request.user)
        context['tasks'] = tasks.sorted('complete')
        myFilter = TaskFilter(self.request.GET, queryset=tasks)

        # search_input = self.request.GET.get('search-area') or ''
        # if(search_input):
        #     context['tasks'] = context['tasks'].filter(
        #         title__startswith=search_input)

        # context['search_area'] = search_input
        context['tasks'] = myFilter.qs
        context['myFilter'] = myFilter

        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('base:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('base:index')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('base:index')
