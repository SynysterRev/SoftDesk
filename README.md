# SoftDesk - API de Gestion de Projets

Une API REST complète pour la gestion de projets collaboratifs, développée avec Django REST Framework.

## Fonctionnalités

- **Authentification JWT** sécurisée
- **Gestion de projets** avec CRUD complet
- **Système de tickets/issues** 
- **Gestion des contributeurs** et permissions
- **API RESTful** avec documentation Postman
- **Permissions granulaires** par rôle

## Technologies

- Python 3.12
- Django REST Framework
- JWT Authentication
- Poetry pour la gestion des dépendances
- PostgreSQL/SQLite

## Documentation de l'API
https://documenter.getpostman.com/view/40327893/2sAYXBEyWR

## Installation
1. Clonez le dépôt ou télécharger une archive.
2. Rendez-vous depuis un terminal dans la racine du répertoire
   - Sur windows : clic-droit puis ouvrir dans le terminal.
   - Sur Mac : ouvrir un terminal puis glisser-déposer le dossier directement dans le terminal.
3. Installer poetry si vous le n'avez pas ```pip install poetry```
4. Créer l'environnement virtuel et installer les dépendances avec ```poetry install```
5. Activez l'environnement virtuel avec ```.venv\Scripts\activate.bat``` sous windows ou ```eval $(poetry env activate)``` sous macos ou linux. (au besoin https://python-poetry.org/docs/managing-environments/#activating-the-environment)
6. Démarrez le serveur avec ```$ python manage.py runserver```

## Utilisateurs
| Nom utilisateur | Mot de passe |
| ------------- | ------------- |
| admin  | admin  |
| presentation_user  | test0123  |
| staff_user | test0123 |
