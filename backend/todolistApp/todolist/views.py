from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task
from .forms import TaskForm
from django.views.decorators.http import require_POST


@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "todolist/dashboard.html", {"tasks": tasks, "form": TaskForm()})


@require_POST
@login_required
def add_task(request):
    if request.method == "POST":
        f = TaskForm(request.POST)
        if f.is_valid():
            t = f.save(commit=False)
            t.user = request.user
            t.save()
    return redirect("todolist:dashboard")

@login_required
def delete_task(request, pk):
    t = get_object_or_404(Task, pk=pk, user=request.user)
    t.delete()
    return redirect("todolist:dashboard")

@login_required
def toggle_task(request, pk):
    t = get_object_or_404(Task, pk=pk, user=request.user)
    t.done = not t.done
    t.completed_at = timezone.now() if t.done else None
    t.save()
    return redirect("todolist:dashboard")