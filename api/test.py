from api.model_patient import Patient

p = Patient(nom="Dupont", prenom="Jean", ssn="191019191000187")
print(p)
print(p.get_sexe())
print(p.get_departement_naissance())