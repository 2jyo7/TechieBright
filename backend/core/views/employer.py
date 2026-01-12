from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from core.models import EmployeeData
from core.utils.auth import employer_required


# ===============================
# EMPLOYER VIEWS
# ===============================

@employer_required
def get_employees(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    employees = EmployeeData.objects.all().values()
    return JsonResponse(list(employees), safe=False)


@employer_required
@csrf_exempt
def add_employee(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)

        emp = EmployeeData.objects.create(
            country=data.get("country", "Unknown"),
            job_title=data.get("job_title", "Unknown"),
            age=data.get("age", 0),
            race=data.get("race", "Not Specified"),
            experience_years=data.get("experience_years", 0),
            salary=data.get("salary", 0),
            industry=data.get("industry", "General"),
            work_type=data.get("work_type", "remote"),
        )

        return JsonResponse({
            "message": "Employee added!",
            "id": emp.id
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)




