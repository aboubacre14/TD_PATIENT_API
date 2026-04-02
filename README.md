# TD API REST - Gestion de Patients

## Description

Ce projet a pour objectif de développer une API REST permettant de gérer des patients à partir d'un fichier JSON.  
L'application est développée en Python avec **FastAPI** et comprend également une **application cliente graphique Tkinter**.

Les données sont stockées dans un fichier JSON partagé entre conteneurs Docker.

---

# Technologies utilisées

- Python
- FastAPI
- Pydantic
- Tkinter
- Requests
- Docker
- Docker Compose
---

# Fonctionnalités de l'API

L'API permet de gérer les patients via plusieurs endpoints REST.

## Endpoints

### Récupérer tous les patients

```
GET /patients
```

### Ajouter un patient

```
POST /patients
```

### Récupérer un patient via son SSN

```
GET /patients/{ssn}
```

### Modifier un patient

```
PATCH /patients/{ssn}
```

### Supprimer un patient

```
DELETE /patients/{ssn}
```

### Ajouter un patient via un endpoint spécifique

```
POST /patients/{ssn}
```

---

# Validation du SSN

Le numéro de sécurité sociale est validé via **Pydantic** :

- 15 chiffres
- premier chiffre :  
  - 1 = homme  
  - 2 = femme
- vérification du mois
- vérification du département
- vérification de la **clé de contrôle modulo 97**

---

# Restriction métier

L'API n'accepte que les patients **nés dans le département 91 (Essonne)**.

---

# Lancer l'API en local

Installer les dépendances :

```bash
pip install -r requirements.txt

Lancer le serveur : python -m uvicorn api.app:app --reload --port 3000

Accéder à la documentation Swagger : http://127.0.0.1:3000/docs

Lancer avec Docker

Construire et lancer les conteneurs : docker compose up --build

L'API sera accessible sur : http://localhost:3000/docs

Application cliente

Une interface graphique a été développée avec Tkinter.

Fonctionnalités :

lecture des patients
ajout d'un patient
modification d'un patient

Lancer l'application : python client/gui.py

