import csv
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "core", "datasets")

alias_map_path = os.path.join(DATASET_DIR, "skill_alias_map.json")

if os.path.exists(alias_map_path):
    with open(alias_map_path, encoding="utf-8") as f:
        alias_map = json.load(f)
else:
    alias_map = {}

INPUT_CSV = os.path.join(DATASET_DIR, "kaggle_software_jobs.csv")
OUTPUT_JSON = os.path.join(DATASET_DIR, "skill_demand.json")

skill_counter = {}

with open(INPUT_CSV, encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader, None)  # skip header row

    for row in reader:
        if len(row) < 4:
            continue

        skills_cell = row[-1]
        if not skills_cell:
            continue

        skills = skills_cell.split(";")

        for skill in skills:
            raw_skill = skill.strip()
            skill = alias_map.get(raw_skill, raw_skill)

            if not skill:
                continue

            skill_counter[skill] = skill_counter.get(skill, 0) + 1

# normalize demand score (0–1)
max_count = max(skill_counter.values())

skill_demand = {
    skill: round(count / max_count, 2)
    for skill, count in skill_counter.items()
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(skill_demand, f, indent=2)

print("✅ skill_demand.json generated successfully")
