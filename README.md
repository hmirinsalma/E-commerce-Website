# CosmoLux — Boutique en ligne de produits cosmétiques

CosmoLux est une application web e-commerce développée avec Django, HTML/CSS, JavaScript et MySQL. Elle permet la gestion d’un catalogue de produits cosmétiques, la gestion des commandes et le suivi des utilisateurs.

## Fonctionnalités principales

- Authentification : inscription, connexion, récupération de mot de passe  
- Catalogue des produits avec filtres par catégorie  
- Gestion du panier (localStorage + synchronisation serveur)  
- Passage de commande avec choix du mode de livraison et paiement (en ligne ou à la livraison)  
- Historique des commandes et gestion du profil utilisateur  
- Interface d'administration via Django Admin  

## Structure du projet

ANA /
├── env/
├── projet/
├── README.md
├── requirements.txt
├── .gitignore

## Prérequis

- Python 3.11+
- Django 4.x
- MySQL (via XAMPP)

## Installation

1. Cloner le projet :

```bash
git clone https://github.com/salmadevellop/cosmolux.git
cd cosmolux

Créer et activer un environnement virtuel :

python -m venv env
env\Scripts\activate

Installer les dépendances :

pip install -r requirements.txt

Configurer MySQL dans settings.py :

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cosmolux_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
Appliquer les migrations et créer le superutilisateur :

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

Lancer le serveur :
python manage.py runserver
