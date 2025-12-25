from core.services.dataset_loader import load_dataset

ROLES = load_dataset("roles.json", "global_data")
SKILLS = load_dataset("skills.json", "global_data")

# Build skill → role map dynamically
SKILL_ROLE_MAP = {}

for role in ROLES:
    for skill in role.get("required_skills", []):
        SKILL_ROLE_MAP.setdefault(skill, []).append(role["title"])
