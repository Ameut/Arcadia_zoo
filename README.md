# Arcadia_zoo
application web d'un projet zoo avec le framawork Django
Projet zoo Arcadia pour ecf 2024
Aperçu du projet
Zoo Arcadia est une application web conçue pour améliorer l'interaction des visiteurs en fournissant des informations détaillées sur les habitats des animaux et les services du zoo. L'application met l'accent sur les thèmes écologiques, reflétant l'engagement du zoo envers la durabilité.

Pile technologique
Frontend : HTML, CSS (Bootstrap), JavaScript
Backend : Django (Python)
Bases de données :
Relationnelle : SQLite3
NoSQL : MongoDB
Contrôle de version : Git
Configuration locale
Cloner le dépôt :
bash
Copy code
git clone https://github.com/Ameut/Arcadia_zoo
cd zooarcadia
Installer les dépendances :
bash
Copy code
pip install -r requirements.txt
Configurer les bases de données :
SQLite est configurée par défaut avec Django.
Pour MongoDB, assurez-vous que MongoDB fonctionne localement ou connectez-vous à une instance MongoDB Atlas. Mettez à jour la chaîne de connexion dans settings.py.
Lancer les migrations :
bash
Copy code
python manage.py migrate
Démarrer le serveur de développement :
bash
Copy code
python manage.py runserver
Accéder à l'application à http://127.0.0.1:8000
Fonctionnalités
Vues interactives des habitats des animaux et détails.
Services aux visiteurs tels que les points de restauration, les visites guidées et les petits tours en train.
Interface administrative pour le personnel du zoo pour gérer les détails des animaux, les services et les rôles des utilisateurs.
Système d'authentification pour le personnel et les administrateurs.
Système de feedback permettant aux visiteurs de laisser des avis, gérés par l'approbation du personnel.
Contribution




Contact
Pour toute question, veuillez contacter ameur.ouafi@hotmail.fr
