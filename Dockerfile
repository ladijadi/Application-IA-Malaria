# Image de base
FROM python:3.11-slim

# Installer les dépendances nécessaires pour le serveur Web
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de l'application
WORKDIR /app
COPY . /app

# Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port
EXPOSE 5000

# Commande pour lancer l'application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.run_app:app"]
