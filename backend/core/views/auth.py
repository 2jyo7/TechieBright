from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from core.models import Profile, EmployeeData



# ===============================
# SIGN UP
# ===============================
@csrf_exempt
def signup_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")
        role = data.get("role")  # "employee" | "employer"

        # ---------------------------
        # Validation
        # ---------------------------
        if not username or not password or not role:
            return JsonResponse({"error": "All fields are required"}, status=400)

        if role not in ["employee", "employer"]:
            return JsonResponse({"error": "Invalid role"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        # ---------------------------
        # Create User
        # ---------------------------
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # ---------------------------
        # Create Profile
        # ---------------------------
        Profile.objects.create(
            user=user,
            role=role
        )

        # ---------------------------
        # Create EmployeeData (ONLY for employees)
        # ---------------------------
        if role == "employee":
            EmployeeData.objects.create(
                user=user,
                country="",
                job_title="",
                age=0,
                race="",
                experience_years=0,
                salary=0,
                industry="",
                work_type="remote",
                skills=[]
            )

        # ---------------------------
        # Auto login after signup
        # ---------------------------
        login(request, user)

        return JsonResponse({
            "message": "Account created",
            "username": user.username,
            "role": role
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
# ===============================
# LOGIN
# ===============================
@csrf_exempt
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
            "message": "Logged in",
            "username": user.username,
            "role": user.profile.role
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ===============================
# LOGOUT
# ===============================
@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})


# ===============================
# CURRENT USER (SESSION CHECK)
# ===============================
def me(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False})

    return JsonResponse({
        "authenticated": True,
        "username": request.user.username,
        "role": request.user.profile.role
    })
