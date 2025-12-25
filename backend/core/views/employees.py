from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.models import EmployeeData


def get_employees(request):
    if request.method == "GET":
        employees = EmployeeData.objects.all().values()
        return JsonResponse(list(employees), safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)



# Get employee by ID - an API endpoint to maintain dashboard for a single employee

def get_employee_by_id(request, user_id):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        emp = EmployeeData.objects.get(id=user_id)
        return JsonResponse({
            "id": emp.id,
            "country": emp.country,
            "job_title": emp.job_title,
            "age": emp.age,
            "race": emp.race,
            "experience_years": emp.experience_years,
            "salary": emp.salary,
            "industry": emp.industry,
            "work_type": emp.work_type,
            "skills": emp.skills or []
        })
    except EmployeeData.DoesNotExist:
        return JsonResponse({"error": "Employee not found"}, status=404)



@csrf_exempt
def add_employee(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Apply backend-safe defaults for missing fields
            country = data.get("country", "Unknown")
            job_title = data.get("job_title", "Unknown")
            age = data.get("age", 0)
            race = data.get("race", "Not Specified")
            experience_years = data.get("experience_years", 0)
            salary = data.get("salary", 0)
            industry = data.get("industry", "General")
            work_type = data.get("work_type", "remote")

            emp = EmployeeData.objects.create(
                country=country,
                job_title=job_title,
                age=age,
                race=race,
                experience_years=experience_years,
                salary=salary,
                industry=industry,
                work_type=work_type
            )

            return JsonResponse({
                "message": "Employee added!",
                "id": emp.id
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def update_skills_by_user(request, user_id):
    try:
        emp = EmployeeData.objects.get(user_id=user_id)
    except EmployeeData.DoesNotExist:
        return JsonResponse({"error": "Employee not found"}, status=404)

    if request.method != "PUT":
        return JsonResponse({"error": "Invalid method"}, status=400)

    data = json.loads(request.body)
    emp.skills = data.get("skills", [])
    emp.save()

    return JsonResponse({"message": "Skills updated!"})
