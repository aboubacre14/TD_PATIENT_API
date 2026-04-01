from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.model_patient import Patient
from api.storage import read_json, write_json

app = FastAPI()

JSON_PATH = "api/patients.json"


class PatientUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None


def patient_exists(data: list, ssn: str) -> bool:
    return any(patient["ssn"] == ssn for patient in data)


def find_patient(data: list, ssn: str):
    for patient in data:
        if patient["ssn"] == ssn:
            return patient
    return None


@app.get("/patients")
def get_patients():
    return read_json(JSON_PATH)


@app.post("/patients")
def create_patient(patient: Patient):
    data = read_json(JSON_PATH)

    if patient_exists(data, patient.ssn):
        raise HTTPException(
            status_code=400,
            detail=f"Création impossible : un patient avec le ssn {patient.ssn} existe déjà."
        )

    data.append(patient.model_dump())
    write_json(JSON_PATH, data)
    return {
        "message": "Patient ajouté avec succès.",
        "patient": patient
    }


@app.get("/patients/{ssn}")
def get_patient_by_ssn(ssn: str):
    data = read_json(JSON_PATH)
    patient = find_patient(data, ssn)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail=f"Aucun patient trouvé avec le ssn {ssn}."
        )

    return patient


@app.delete("/patients/{ssn}")
def delete_patient(ssn: str):
    data = read_json(JSON_PATH)
    patient = find_patient(data, ssn)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail=f"Suppression impossible : aucun patient trouvé avec le ssn {ssn}."
        )

    new_data = [p for p in data if p["ssn"] != ssn]
    write_json(JSON_PATH, new_data)

    return {
        "message": f"Le patient avec le ssn {ssn} a été supprimé avec succès."
    }


@app.patch("/patients/{ssn}")
def update_patient(ssn: str, patient_update: PatientUpdate):
    data = read_json(JSON_PATH)
    patient = find_patient(data, ssn)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail=f"Mise à jour impossible : aucun patient trouvé avec le ssn {ssn}."
        )

    if patient_update.nom is None and patient_update.prenom is None:
        raise HTTPException(
            status_code=400,
            detail="Mise à jour impossible : aucun champ à modifier n'a été fourni."
        )

    if patient_update.nom is not None:
        patient["nom"] = patient_update.nom

    if patient_update.prenom is not None:
        patient["prenom"] = patient_update.prenom

    write_json(JSON_PATH, data)

    return {
        "message": f"Le patient avec le ssn {ssn} a été mis à jour avec succès.",
        "patient": patient
    }


@app.post("/patients/{ssn}")
def create_patient_with_ssn(ssn: str, patient: Patient):
    data = read_json(JSON_PATH)

    if patient_exists(data, ssn):
        raise HTTPException(
            status_code=400,
            detail=f"Création impossible : un patient avec le ssn {ssn} existe déjà."
        )

    if patient.ssn != ssn:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Incohérence détectée : le ssn de l'URL ({ssn}) "
                f"est différent du ssn du body ({patient.ssn})."
            )
        )

    data.append(patient.model_dump())
    write_json(JSON_PATH, data)

    return {
        "message": "Patient ajouté avec succès via l'endpoint ciblé.",
        "patient": patient
    }