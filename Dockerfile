# Utiliser une image de base officielle de Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt
COPY requirements.txt .

# Mettre à jour pip
RUN pip install --upgrade pip

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le contenu du projet dans le répertoire de travail
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port 8000
EXPOSE 8000

# Commande par défaut pour démarrer l'application
CMD ["gunicorn", "zooArcadia.wsgi:application", "--bind", "0.0.0.0:8000"]
