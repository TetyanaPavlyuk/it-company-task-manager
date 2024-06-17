from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import (
    WorkerCreationForm,
    WorkerUpdateForm,
    TaskForm,
    PositionSearchForm,
    WorkerSearchForm,
    TaskTypeSearchForm,
    TaskSearchForm,
    NewForm,
)
from .models import Position, Worker, TaskType, Task, New


@login_required
def index(request):
    """View function for the home page of the site"""
    num_experts = Worker.objects.count()
    num_completed_tasks = Task.objects.filter(is_completed=True).count()
    num_defined_tasks = Task.objects.filter(is_completed=False).count()
    new_list = New.objects.all()

    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_experts": num_experts,
        "num_completed_tasks": num_completed_tasks,
        "num_defined_tasks": num_defined_tasks,
        "num_visits": num_visits,
        "new_list": new_list,
    }

    return render(request, "task_manager/index.html", context=context)


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    template_name = "task_manager/position_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        model = self.request.GET.get("model", "")

        context["search_form"] = PositionSearchForm(
            initial={"model": model}
        )
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["model"]
            )
        return queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    queryset = Worker.objects.all().select_related("position")
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        model = self.request.GET.get("model", "")

        context["search_form"] = WorkerSearchForm(
            initial={"model": model}
        )
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.select_related("position")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                Q(username__icontains=form.cleaned_data["model"]) |
                Q(first_name__icontains=form.cleaned_data["model"]) |
                Q(last_name__icontains=form.cleaned_data["model"]) |
                Q(position__name__icontains=form.cleaned_data["model"])
            )
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()
        tasks = (Task.objects.prefetch_related("assignees").
                 filter(assignees__exact=worker))
        context["tasks_completed"] = tasks.filter(is_completed=True)
        context["task_defined"] = tasks.filter(is_completed=False)
        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task_manager:worker-list")

    def get_queryset(self):
        return Worker.objects.filter(username=self.request.user.username)


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "task_manager/tasktype_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        model = self.request.GET.get("model", "")

        context["search_form"] = TaskTypeSearchForm(
            initial={"model": model}
        )
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["model"]
            )
        return queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = (Task.objects.all().select_related("task_type").
                prefetch_related("assignees"))
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        model = self.request.GET.get("model", "")

        context["search_form"] = TaskSearchForm(
            initial={"model": model}
        )
        return context

    def get_queryset(self):
        queryset = (Task.objects.select_related("task_type").
                    prefetch_related("assignees"))
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["model"]
            )
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class NewCreateView(LoginRequiredMixin, generic.CreateView):
    model = New
    form_class = NewForm
    success_url = reverse_lazy("task_manager:index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = New
    form_class = NewForm
    success_url = reverse_lazy("task_manager:index")

    def get_queryset(self):
        return New.objects.filter(author=self.request.user)


class NewDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = New
    success_url = reverse_lazy("task_manager:index")
