from django.urls import path
from . import views

app_name = "todolist"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("add/", views.add_task, name="add_task"),
    path("<int:pk>/toggle/", views.toggle_task, name="toggle_task"),
    path("<int:pk>/delete/", views.delete_task, name="delete_task"),
]