from core.services.global_data_service import ROLES
from core.services.dataset_cache import SKILL_DEMAND

def analyze_skill_gap(employee_skills, target_role_title):
    role = next(
        (r for r in ROLES if r["title"] == target_role_title),
        None
    )

    if not role:
        return None

    required = set(role["required_skills"])
    current = set(employee_skills)

    matched = list(required & current)
    missing = list(required - current)

    enriched_missing = []

    for skill in missing:
        demand = SKILL_DEMAND.get(skill, 0.5)
        priority = (
            "High" if demand > 0.75
            else "Medium" if demand > 0.4
            else "Low"
        )

        enriched_missing.append({
            "skill": skill,
            "demand_score": demand,
            "priority": priority
        })

    return {
        "role": target_role_title,
        "matched_skills": matched,
        "missing_skills": enriched_missing
    }
