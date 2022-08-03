from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegistrationForm

from django.contrib.auth import login, authenticate

from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import Task


class CustomLoginView(LoginView):
    fields = '__all__'
    template_name = 'base/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('base:index')

# def register_view(request, *args, **kwargs):
#     user = request.user
#     if user.is_authenticated:
#         return redirect('base:index',  *args, **kwargs)
#     context = {}
#     if request.POST:
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email').lower()
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(email=email, password=raw_password)
#             login(request, user)
#             return  redirect('base:index')
#         else:
#             context['registration_form'] = form
#     return render(request, 'base/register.html',  context)

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
            auth_user = authenticate(email=email, password=raw_password)
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
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['tasks'] = context['tasks'].sorted('complete')

        search_input = self.request.GET.get('search-area') or ''
        if(search_input):
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input)

        context['search_area'] = search_input

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
