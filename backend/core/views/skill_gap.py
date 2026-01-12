from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from core.models import EmployeeData
from core.services.skill_gap_service import analyze_skill_gap
from core.utils.auth import employee_required


@employee_required
@csrf_exempt
def skill_gap_analysis(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    try:
        data = json.loads(request.body)
        target_role = data.get("role")

        if not target_role:
            return JsonResponse(
                {"error": "Target role is required"},
                status=400
            )

        # 🔒 Always use logged-in user
        emp = EmployeeData.objects.get(user=request.user)

        result = analyze_skill_gap(
            emp.skills or [],
            target_role
        )

        return JsonResponse(result)

    except EmployeeData.DoesNotExist:
        return JsonResponse(
            {"error": "Employee profile not found"},
            status=404
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )
