from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, os

from core.models import Recommendation
from core.services.global_data_service import SKILL_ROLE_MAP, SKILLS, ROLES
from core.services.dataset_cache import SKILL_DEMAND, SALARY_DATA
from core.utils.auth import employee_required

from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ===============================
# Helpers
# ===============================

def safe_parse_json(text):
    try:
        return json.loads(text)
    except Exception:
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end+1])
            except Exception:
                pass
    return None


# ===============================
# AI Recommendation (EMPLOYEE)
# ===============================

@employee_required
@csrf_exempt
def ai_recommendation(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        input_query = data.get("query")

        if not input_query:
            return JsonResponse({"error": "Query is required"}, status=400)

        user = request.user

        prompt = f"""
You are an IT career advisor. You must output ONLY a valid JSON object.

Format:
{{
  "skills": [],
  "roles": [],
  "roadmap": [],
  "notes": ""
}}

GLOBAL_SKILLS = {SKILLS}
GLOBAL_ROLES = {[r["title"] for r in ROLES]}

User query: "{input_query}"

Pick skills and roles ONLY from the global lists.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
        )

        raw = response.choices[0].message.content
        parsed = safe_parse_json(raw)

        if not parsed:
            return JsonResponse(
                {"error": "AI did not return valid JSON"},
                status=502
            )

        parsed.setdefault("skills", [])
        parsed.setdefault("roles", [])
        parsed.setdefault("roadmap", [])
        parsed.setdefault("notes", "")

        # ===============================
        # Dataset enrichment
        # ===============================

        dataset_insights = []

        for skill in parsed["skills"]:
            demand = SKILL_DEMAND.get(skill, 0.5)
            dataset_insights.append({
                "skill": skill,
                "demand_score": demand,
                "avg_salary": SALARY_DATA.get(skill, 500000),
                "market_note": "High demand" if demand > 0.75 else "Moderate demand"
            })

        parsed["dataset_insights"] = dataset_insights

        # ===============================
        # Role matching
        # ===============================

        matched_roles = set()
        for skill in parsed["skills"]:
            matched_roles.update(SKILL_ROLE_MAP.get(skill, []))

        parsed["matched_roles"] = list(matched_roles)

        # ===============================
        # Save recommendation
        # ===============================

        Recommendation.objects.create(
            user=user,
            input_query=input_query,
            ai_response=json.dumps(parsed, ensure_ascii=False)
        )

        return JsonResponse({"recommendation": parsed})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ===============================
# Recommendation History (EMPLOYEE)
# ===============================

@employee_required
def get_recommendations(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    recs = Recommendation.objects.filter(user=request.user).order_by("-created_at")

    output = []
    for rec in recs:
        try:
            parsed = json.loads(rec.ai_response)
        except Exception:
            parsed = {}

        output.append({
            "id": rec.id,
            "query": rec.input_query,
            "response": parsed,
            "created_at": rec.created_at.isoformat()
        })

    return JsonResponse(output, safe=False)


# ===============================
# Delete Recommendation (EMPLOYEE)
# ===============================

@employee_required
@csrf_exempt
def delete_recommendation(request, rec_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        rec = Recommendation.objects.get(id=rec_id, user=request.user)
        rec.delete()
        return JsonResponse({"message": "Deleted successfully"})
    except Recommendation.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)


# ===============================
# Edit Recommendation (EMPLOYEE)
# ===============================

@employee_required
@csrf_exempt
def edit_recommendation(request, rec_id):
    if request.method != "PUT":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        body = json.loads(request.body)
        new_query = body.get("query")

        if not new_query:
            return JsonResponse({"error": "Query cannot be empty"}, status=400)

        rec = Recommendation.objects.get(id=rec_id, user=request.user)
        rec.input_query = new_query
        rec.save()

        return JsonResponse({"message": "Updated successfully"})

    except Recommendation.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)
