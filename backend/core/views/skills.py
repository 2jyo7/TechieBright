from django.http import JsonResponse
from core.models import Skill


def get_skills(request):
    if request.method == "GET":
        skills = Skill.objects.all().values()
        return JsonResponse(list(skills), safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=400)
