# core/views/ai.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from core.models import Recommendation
from core.services.global_data_service import SKILL_ROLE_MAP, SKILLS, ROLES
from core.services.dataset_cache import SKILL_DEMAND, SALARY_DATA

import json, os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def safe_parse_json(text):
    """
    Try to extract JSON from model response. If model wraps it in backticks
    or text, try to find the first { ... } substring.
    """
    try:
        return json.loads(text)
    except Exception:
        # attempt to find JSON substring
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end+1])
            except Exception:
                pass
    return None


@csrf_exempt
def ai_recommendation(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        input_query = data.get("query")
        user = User.objects.get(id=user_id)

        # Enhanced Prompt with Global Context
        prompt = f"""
You are an IT career advisor. You must output ONLY a valid JSON object with no explanations.

Use this structured JSON format EXACTLY:

{{
  "skills": ["skill1", "skill2", ...],
  "roles": ["role1", "role2"],
  "roadmap": ["step 1", "step 2", ...],
  "notes": "short helpful comment"
}}

GLOBAL_SKILLS = {SKILLS}
GLOBAL_ROLES = {[role["title"] for role in ROLES]}

User query: "{input_query}"

Pick skills and roles ONLY from the global lists.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role":"system","content":"You MUST output only valid JSON."},
                {"role":"user","content":prompt}
            ],
            temperature=0.0,
        )

        raw = response.choices[0].message.content
        parsed = safe_parse_json(raw)

        # Guarantee valid structure
        if not parsed:
            return JsonResponse({"error":"AI did not return valid JSON", "raw": raw}, status=502)

        parsed.setdefault("skills", [])
        parsed.setdefault("roles", [])
        parsed.setdefault("roadmap", [])
        parsed.setdefault("notes", "")


        # ---- DATASET ENRICHMENT START ----

        skill_demand = SKILL_DEMAND
        salary_data = SALARY_DATA


        dataset_insights = []

        for skill in parsed["skills"]:
            dataset_insights.append({
               "skill": skill,
           "demand_score": skill_demand.get(skill, 0.5),
           "avg_salary": salary_data.get(skill, 500000),
           "market_note": (
            "High demand skill"
            if skill_demand.get(skill, 0.5) > 0.75
            else "Moderate demand"
              )
           })

            parsed["dataset_insights"] = dataset_insights

# ---- DATASET ENRICHMENT END ----


        # Add dataset-based role matching
        matched_roles = set()
        for skill in parsed["skills"]:
            roles = SKILL_ROLE_MAP.get(skill, [])
            matched_roles.update(roles)

        parsed["matched_roles"] = list(matched_roles)

        # Save to DB
        Recommendation.objects.create(
            user=user,
            input_query=input_query,
            ai_response=json.dumps(parsed, ensure_ascii=False)
        )

        return JsonResponse({"recommendation": parsed})

    except User.DoesNotExist:
        return JsonResponse({"error":"User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)




def get_recommendations(request, user_id):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        recs = Recommendation.objects.filter(user_id=user_id)

        output = []

        for rec in recs:
            try:
                print("RAW AI RESPONSE:", rec.ai_response)  # DEBUG
                parsed = json.loads(rec.ai_response)
            except Exception as e:
                print("JSON PARSE ERROR:", e)  # DEBUG
                parsed = {
                    "skills": [],
                    "roles": [],
                    "roadmap": [],
                    "notes": "Invalid stored JSON"
                }

            try:
                created = rec.created_at.isoformat()
            except Exception as e:
                print("DATETIME ERROR:", e)  # DEBUG
                created = None

            output.append({
                "id": rec.id,
                "query": rec.input_query,
                "response": parsed,
                "created_at": created,
            })

        return JsonResponse(output, safe=False)

    except Exception as e:
        print("\n🔴 ERROR in get_recommendations:", e, "\n")   # ← PRINT ACTUAL PROBLEM
        raise e  # ← show full traceback in console


# Delete endpoint for ai recommendations history
@csrf_exempt
def delete_recommendation(request, rec_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        rec = Recommendation.objects.get(id=rec_id)
        rec.delete()
        return JsonResponse({"message": "Deleted successfully"})
    
    except Recommendation.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
#edit endpoint for ai recommendations history
@csrf_exempt
def edit_recommendation(request, rec_id):
    if request.method != "PUT":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        body = json.loads(request.body)
        new_query = body.get("query")

        if not new_query:
            return JsonResponse({"error": "Query cannot be empty"}, status=400)

        rec = Recommendation.objects.get(id=rec_id)
        rec.input_query = new_query
        rec.save()

        return JsonResponse({"message": "Updated successfully"})

    except Recommendation.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
