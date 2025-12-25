from django.http import JsonResponse
from core.services.global_data_service import SKILLS, ROLES, SKILL_ROLE_MAP

def get_global_skills(request):
    return JsonResponse(SKILLS, safe=False)

def get_global_roles(request):
    return JsonResponse(ROLES, safe=False)

def get_skill_role_map(request):
    return JsonResponse(SKILL_ROLE_MAP, safe=False)
