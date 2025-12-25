import json
import os
from django.conf import settings


def load_dataset(filename, subdir):
    """
    filename: roles.json, skills.json, etc.
    subdir: 'datasets' or 'global_data'
    """
    path = os.path.join(
        settings.BASE_DIR,
        "core",
        subdir,
        filename
    )

    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
