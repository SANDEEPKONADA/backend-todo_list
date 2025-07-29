from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.db import transaction
from django.http import HttpResponseRedirect

from .models import Task, TaskMedia
from .forms import TaskForm, TaskMediaForm, PositionForm


# 🔐 Login View
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


# 📝 Register View
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


# 📋 Task List View
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context


# 📄 Task Detail View
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


# ➕ Task Create View
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'base/task_form.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_form'] = TaskMediaForm()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        files = self.request.FILES.getlist('files')
        for f in files:
            TaskMedia.objects.create(task=self.object, file=f)

        return response


# ✏️ Task Update View
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'base/task_form.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_form'] = TaskMediaForm()
        context['existing_files'] = TaskMedia.objects.filter(task=self.object)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        files = self.request.FILES.getlist('files')
        for f in files:
            TaskMedia.objects.create(task=self.object, file=f)
        return response


# 🗑️ Task Delete View
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


# 🔀 Task Reorder View
class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            position_list = form.cleaned_data["position"].split(',')
            with transaction.atomic():
                self.request.user.set_task_order(position_list)

        return redirect('tasks')


# ❌ Delete Media File View
class TaskFileDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        file = get_object_or_404(TaskMedia, pk=pk)
        if file.task.user == request.user:
            file.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
