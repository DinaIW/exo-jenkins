FROM python:3.8

WORKDIR /app

# Mettre à jour pip
RUN pip install --upgrade pip

# Installation des dépendances nécessaires pour la compilation
RUN apt-get update && apt-get install -y gcc python3-dev

# Copier les fichiers nécessaires dans le conteneur
COPY build/movie-service/app ./app
COPY build/movie-service/main.py .
COPY build/movie-service/requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
