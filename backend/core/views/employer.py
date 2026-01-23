from django.http import JsonResponse
import json

from core.models import EmployeeData
from core.utils.auth import employer_required


# ===============================
# GET EMPLOYEES (READ-ONLY → NO CSRF NEEDED)
# ===============================
@employer_required
def get_employees(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    employees = EmployeeData.objects.all().values(
        "id",
        "country",
        "job_title",
        "age",
        "race",
        "experience_years",
        "salary",
        "industry",
        "work_type",
        "user_id",
    )

    return JsonResponse(list(employees), safe=False)


# ===============================
# ADD EMPLOYEE (CSRF-PROTECTED)
# ===============================
@employer_required
def add_employee(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)

        emp = EmployeeData.objects.create(
            user=None,  # explicit is better than implicit
            country=data.get("country", ""),
            job_title=data.get("job_title", ""),
            age=data.get("age", 0),
            race=data.get("race", ""),
            experience_years=data.get("experience_years", 0),
            salary=data.get("salary", 0),
            industry=data.get("industry", ""),
            work_type=data.get("work_type", "remote"),
            skills=data.get("skills", []),
        )

        return JsonResponse({
            "message": "Employee added",
            "id": emp.id
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
