from django.http import JsonResponse

def employee_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        if not hasattr(request.user, "profile"):
            return JsonResponse({"error": "Profile missing"}, status=403)

        if request.user.profile.role != "employee":
            return JsonResponse({"error": "Forbidden"}, status=403)

        return view_func(request, *args, **kwargs)

    return wrapper


def employer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        if not hasattr(request.user, "profile"):
            return JsonResponse({"error": "Profile missing"}, status=403)

        if request.user.profile.role != "employer":
            return JsonResponse({"error": "Forbidden"}, status=403)

        return view_func(request, *args, **kwargs)

    return wrapper
