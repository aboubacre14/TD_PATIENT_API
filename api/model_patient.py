from pydantic import BaseModel, field_validator


class Patient(BaseModel):
    nom: str
    prenom: str
    ssn: str

    @field_validator("ssn")
    @classmethod
    def validate_ssn(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("Le ssn doit contenir uniquement des chiffres.")

        if len(value) != 15:
            raise ValueError("Le ssn doit contenir exactement 15 chiffres.")

        if value[0] not in {"1", "2"}:
            raise ValueError("Le premier chiffre du ssn doit être 1 ou 2.")

        month = int(value[3:5])
        if month < 1 or month > 12:
            raise ValueError("Le mois de naissance est invalide.")

        department = value[5:7]
        if not department.isdigit():
            raise ValueError("Le département de naissance doit être numérique.")

        first_thirteen = int(value[:13])
        control_key = int(value[13:15])

        expected_key = 97 - (first_thirteen % 97)
        if expected_key == 97:
            expected_key = 0

        if control_key != expected_key:
            raise ValueError("La clé de contrôle du ssn est invalide.")

        return value

    def get_sexe(self) -> str:
        return "homme" if self.ssn[0] == "1" else "femme"

    def get_annee_naissance(self) -> str:
        return self.ssn[1:3]

    def get_mois_naissance(self) -> str:
        return self.ssn[3:5]

    def get_departement_naissance(self) -> str:
        return self.ssn[5:7]

    def get_identifiant_pays_naissance(self) -> str:
        return self.ssn[7:10]

    def get_indice_naissance(self) -> str:
        return self.ssn[10:13]

    def get_numero_insee(self) -> str:
        return self.ssn[:13]

    def get_identifiant_enregistrement(self) -> str:
        return self.ssn[7:13]