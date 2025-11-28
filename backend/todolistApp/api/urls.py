from django.urls import path
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from . import views

def api_health(request):
    return JsonResponse({"api": "ok"})

@ensure_csrf_cookie
def csrf_view(request):
    return HttpResponse("ok")

urlpatterns = [
    path("health/", api_health, name="api_health"),
    path("csrf/", csrf_view, name="api_csrf"),

    path("register/", views.register, name="api_register"),
    path("login/", views.login_view, name="api_login"),
    path("logout/", views.logout_view, name="api_logout"),
    path("me/", views.me, name="api_me"),

    path("tasks/", views.tasks_list_create, name="api_tasks_list_create"),
    path("tasks/<int:task_id>/toggle/", views.task_toggle, name="api_task_toggle"),
    path("tasks/<int:task_id>/", views.task_delete, name="api_task_delete"),
]