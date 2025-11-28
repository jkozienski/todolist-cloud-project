import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from todolist.models import Task

User = get_user_model()

@csrf_exempt  # można zdjąć gdy front poprawnie wysyła X-CSRFToken
@require_POST
def register(request):
    data = json.loads(request.body)
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    confirm = data.get("confirm")

    if not all([name, email, password, confirm]):
        return JsonResponse({"ok": False, "error": "missing_fields"}, status=400)
    if password != confirm:
        return JsonResponse({"ok": False, "error": "password_mismatch"}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({"ok": False, "error": "email_taken"}, status=400)

    user = User.objects.create_user(username=email, email=email, password=password)
    user.first_name = name
    user.save()
    return JsonResponse({"ok": True})

@csrf_exempt  # zdjąć gdy front poprawnie wysyła X-CSRFToken
@require_POST
def login_view(request):
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    user = authenticate(request, username=email, password=password)
    if user is None:
        return JsonResponse({"ok": False, "error": "invalid_credentials"}, status=401)

    login(request, user)  # ustawia sessionid
    return JsonResponse({"ok": True})

@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({"ok": True})

@require_GET
def me(request):
    if request.user.is_authenticated:
        return JsonResponse({"auth": True, "user": {"email": request.user.email, "name": request.user.first_name}})
    return JsonResponse({"auth": False}, status=401)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def tasks_list_create(request):
    # GET -> pobierz wszystkie zadania użytkownika
    if request.method == "GET":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "unauthorized"}, status=401)
        tasks = list(Task.objects.filter(user=request.user).values("id", "title", "done"))
        return JsonResponse(tasks, safe=False)

    # POST -> dodaj nowe zadanie
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "unauthorized"}, status=401)
        data = json.loads(request.body)
        title = data.get("title")
        if not title:
            return JsonResponse({"error": "missing title"}, status=400)
        task = Task.objects.create(user=request.user, title=title)
        return JsonResponse({"id": task.id, "title": task.title, "done": task.done})
    
@csrf_exempt
@require_http_methods(["POST"])
def task_toggle(request, task_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "unauthorized"}, status=401)
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.done = not task.done
        task.save()
        return JsonResponse({"ok": True, "done": task.done})
    except Task.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)


@csrf_exempt
@require_http_methods(["DELETE"])
def task_delete(request, task_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "unauthorized"}, status=401)
    try:
        Task.objects.get(id=task_id, user=request.user).delete()
        return JsonResponse({"ok": True})
    except Task.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)