from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "done", "created_at", "completed_at")
    list_filter = ("done", "created_at")
    search_fields = ("title", "user__username")