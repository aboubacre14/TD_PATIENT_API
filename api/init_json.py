import os
from api.storage import write_json

JSON_PATH = os.getenv("PATIENTS_JSON_PATH", "api/patients.json")


def main():
    if not os.path.exists(JSON_PATH):
        write_json(JSON_PATH, [])
        print(f"Fichier JSON initialisé : {JSON_PATH}")
    else:
        print(f"Fichier JSON déjà présent : {JSON_PATH}")


if __name__ == "__main__":
    main()