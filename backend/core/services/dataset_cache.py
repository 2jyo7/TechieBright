from core.services.dataset_loader import load_dataset

SKILL_DEMAND = load_dataset("skill_demand.json", "datasets")
SALARY_DATA = load_dataset("salary_data.json", "datasets")
