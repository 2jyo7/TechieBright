from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from core.models import EmployeeData
from core.utils.auth import employee_required


# ===============================
# GET PROFILE
# ===============================
@employee_required
def get_employee_profile(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        emp = EmployeeData.objects.get(user=request.user)
    except EmployeeData.DoesNotExist:
        return JsonResponse({"error": "Profile not found"}, status=404)

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
# UPDATE PROFILE
# ===============================
@employee_required
@csrf_exempt
def update_employee_profile(request):
    if request.method != "PUT":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        emp = EmployeeData.objects.get(user=request.user)
    except EmployeeData.DoesNotExist:
        return JsonResponse({"error": "Profile not found"}, status=404)

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
# DELETE PROFILE (OPTIONAL)
# ===============================
@employee_required
@csrf_exempt
def delete_employee_profile(request):
    if request.method != "DELETE":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        emp = EmployeeData.objects.get(user=request.user)
        emp.delete()
        return JsonResponse({"message": "Profile deleted"})
    except EmployeeData.DoesNotExist:
        return JsonResponse({"error": "Profile not found"}, status=404)

# ===============================
# EMPLOYEE Skills VIEWS
# ===============================

@employee_required
@csrf_exempt
def update_employee_skills(request):
    if request.method != "PUT":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        emp = EmployeeData.objects.get(user=request.user)
    except EmployeeData.DoesNotExist:
        return JsonResponse({"error": "Employee not found"}, status=404)

    data = json.loads(request.body)
    emp.skills = data.get("skills", [])
    emp.save()

    return JsonResponse({"message": "Skills updated!"})
