import json
import os


def read_json(json_path: str):
    if not os.path.exists(json_path):
        raise FileNotFoundError(
            f"Le fichier JSON '{json_path}' est introuvable."
        )

    with open(json_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []

        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Le fichier JSON '{json_path}' contient un JSON invalide."
            ) from exc


def write_json(json_path: str, data):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)