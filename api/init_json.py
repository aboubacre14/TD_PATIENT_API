import os
from api.storage import write_json

JSON_PATH = "/data/patients.json"


def main():
    if not os.path.exists(JSON_PATH):
        write_json(JSON_PATH, [])
        print("Fichier JSON initialisé.")
    else:
        print("Fichier JSON déjà présent.")


if __name__ == "__main__":
    main()