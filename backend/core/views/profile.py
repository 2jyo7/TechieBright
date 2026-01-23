from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json

from core.models import EmployeeData
from core.utils.auth import employee_required


# ===============================
# GET PROFILE (SAFE, NO 404)
# ===============================
@employee_required
def get_employee_profile(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid method"}, status=400)

    emp, _ = EmployeeData.objects.get_or_create(
        user=request.user,
        defaults={
            "country": "",
            "job_title": "",
            "age": 0,
            "race": "",
            "experience_years": 0,
            "salary": 0,
            "industry": "",
            "work_type": "remote",
            "skills": []
        }
    )

    return JsonResponse({
        "country": emp.country,
        "age": emp.age,
        "race": emp.race,
        "job_title": emp.job_title,
        "industry": emp.industry,
        "experience_years": emp.experience_years,
        "salary": emp.salary,
        "work_type": emp.work_type,
        "skills": emp.skills or []
    })


# ===============================
# UPDATE PROFILE (SAFE)
# ===============================
@employee_required
def update_employee_profile(request):
    if request.method != "PUT":
        return JsonResponse({"error": "Invalid method"}, status=400)

    emp, _ = EmployeeData.objects.get_or_create(user=request.user)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    emp.country = data.get("country", emp.country)
    emp.age = data.get("age", emp.age)
    emp.race = data.get("race", emp.race)
    emp.job_title = data.get("job_title", emp.job_title)
    emp.industry = data.get("industry", emp.industry)
    emp.experience_years = data.get("experience_years", emp.experience_years)
    emp.salary = data.get("salary", emp.salary)
    emp.work_type = data.get("work_type", emp.work_type)

    emp.save()

    return JsonResponse({"message": "Profile updated"})


# ===============================
# UPDATE SKILLS (SAFE)
# ===============================
@employee_required
def update_employee_skills(request):
    if request.method != "PUT":
        return JsonResponse({"error": "Invalid method"}, status=400)

    emp, _ = EmployeeData.objects.get_or_create(user=request.user)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    emp.skills = data.get("skills", [])
    emp.save()

    return JsonResponse({"message": "Skills updated"})


# ===============================
# DELETE PROFILE (SAFE)
# ===============================
@employee_required
def delete_employee_profile(request):
    if request.method != "DELETE":
        return JsonResponse({"error": "Invalid method"}, status=400)

    emp = EmployeeData.objects.filter(user=request.user).first()

    if not emp:
        # Profile already doesn't exist → still OK
        return JsonResponse({"message": "Profile already deleted"})

    emp.delete()

    return JsonResponse({"message": "Profile deleted successfully"})