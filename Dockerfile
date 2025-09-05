# Image officielle Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Exposer le port
EXPOSE 80

# Lancer Flask en mode production (debug désactivé)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
