import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:3000"


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application Cliente - Patients")
        self.geometry("700x500")

        # Champ SSN
        tk.Label(self, text="SSN").pack()
        self.ssn_entry = tk.Entry(self, width=50)
        self.ssn_entry.pack(pady=5)

        # Champ Nom
        tk.Label(self, text="Nom").pack()
        self.nom_entry = tk.Entry(self, width=50)
        self.nom_entry.pack(pady=5)

        # Champ Prénom
        tk.Label(self, text="Prénom").pack()
        self.prenom_entry = tk.Entry(self, width=50)
        self.prenom_entry.pack(pady=5)

        # Zone d'affichage
        self.output = tk.Text(self, height=15, width=80)
        self.output.pack(pady=10)

        # Boutons
        button_frame = tk.Frame(self)
        button_frame.pack()

        tk.Button(button_frame, text="Read", command=self.read_data).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Add", command=self.add_value).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Update", command=self.update_value).grid(row=0, column=2, padx=5)

        self.read_data()

    def display_output(self, content):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, content)

    def read_data(self):
        """Read through GET"""
        try:
            response = requests.get(f"{API_URL}/patients")
            response.raise_for_status()
            data = response.json()
            self.display_output(str(data))
        except requests.RequestException as exc:
            messagebox.showerror("Erreur GET", f"Impossible de lire les données : {exc}")

    def add_value(self):
        """Add through POST"""
        ssn = self.ssn_entry.get().strip()
        nom = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()

        if not ssn or not nom or not prenom:
            messagebox.showwarning("Champs manquants", "Veuillez remplir ssn, nom et prénom.")
            return

        payload = {
            "nom": nom,
            "prenom": prenom,
            "ssn": ssn
        }

        try:
            response = requests.post(f"{API_URL}/patients", json=payload)
            if response.status_code >= 400:
                detail = response.json().get("detail", "Erreur inconnue.")
                raise ValueError(detail)

            data = response.json()
            self.display_output(str(data))
            self.read_data()
        except Exception as exc:
            messagebox.showerror("Erreur POST", f"Impossible d'ajouter le patient : {exc}")

    def update_value(self):
        """Update through PATCH"""
        ssn = self.ssn_entry.get().strip()
        nom = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()

        if not ssn:
            messagebox.showwarning("Champs manquants", "Veuillez renseigner le ssn du patient à modifier.")
            return

        payload = {}
        if nom:
            payload["nom"] = nom
        if prenom:
            payload["prenom"] = prenom

        if not payload:
            messagebox.showwarning("Aucune modification", "Veuillez renseigner au moins un champ à modifier.")
            return

        try:
            response = requests.patch(f"{API_URL}/patients/{ssn}", json=payload)
            if response.status_code >= 400:
                detail = response.json().get("detail", "Erreur inconnue.")
                raise ValueError(detail)

            data = response.json()
            self.display_output(str(data))
            self.read_data()
        except Exception as exc:
            messagebox.showerror("Erreur PATCH", f"Impossible de modifier le patient : {exc}")


if __name__ == "__main__":
    app = Application()
    app.mainloop()