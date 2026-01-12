from django.http import JsonResponse
from core.services.global_data_service import SKILLS, ROLES, SKILL_ROLE_MAP


def get_global_skills(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    return JsonResponse(SKILLS, safe=False)


def get_global_roles(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    return JsonResponse(ROLES, safe=False)


def get_skill_role_map(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    return JsonResponse(SKILL_ROLE_MAP, safe=False)
