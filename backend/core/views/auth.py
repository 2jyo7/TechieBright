from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json

from core.models import Profile


# ===============================
# SIGNUP
# ===============================
def signup_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")
        role = data.get("role")

        if not username or not password or not role:
            return JsonResponse({"error": "All fields are required"}, status=400)

        if role not in ["employee", "employer"]:
            return JsonResponse({"error": "Invalid role"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Profile.objects.create(
            user=user,
            role=role
        )

        login(request, user)

        return JsonResponse({
            "authenticated": True,
            "username": user.username,
            "role": role
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ===============================
# LOGIN
# ===============================
@ensure_csrf_cookie
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        data = json.loads(request.body)

        user = authenticate(
            username=data.get("username"),
            password=data.get("password")
        )

        if not user:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

        login(request, user)

        return JsonResponse({
            "authenticated": True,
            "username": user.username,
            "role": user.profile.role
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ===============================
# LOGOUT
# ===============================
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})


# ===============================
# SESSION CHECK (CSRF COOKIE SOURCE)
# ===============================
@ensure_csrf_cookie
def me(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False})

    return JsonResponse({
        "authenticated": True,
        "username": request.user.username,
        "role": request.user.profile.role
    })
