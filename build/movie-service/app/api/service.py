import os
import httpx

# Définir une valeur par défaut pour la variable d'environnement qui utilise le DNS interne de Kubernetes
CAST_SERVICE_HOST_URL = os.getenv('CAST_SERVICE_HOST_URL', 'http://fastapi-cast-service:8000/api/v1/casts/')

def is_cast_present(cast_id: int):
    url = os.environ.get('CAST_SERVICE_HOST_URL') or CAST_SERVICE_HOST_URL
    r = httpx.get(f'{url}{cast_id}', follow_redirects=True)
    return True if r.status_code == 200 else False