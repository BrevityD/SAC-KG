from typing import Dict, Any

import yaml

def load_prompts() -> Dict[str, Any]:
    with open("prompts.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
