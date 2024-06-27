
Lancer le chart :
helm install chart-staging --namespace staging ./chart-staging/ -f ./chart-staging/values.yaml -f ./chart-staging/values-secret.yaml
helm uninstall chart-staging -n staging

ENV QA

-Nouvelle base :
    cast_db_staging
    movie_db_staging

-Nouveau mot de passe plus fort

- Création du ingress laissé en http (cert sera fait en prod)

- augementation des ressources (values.yaml)

- insertion d'une bdd plus conséquente



https://devops.dev-euphony.fr/api/v1/movies/docs#/


apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  default.conf: |
    server {
      listen 8080;

      location /api/v1/movies {
        proxy_pass http://devops.dev-euphony.fr/api/v1/movies;
      }

      location /api/v1/casts {
        proxy_pass http://fastapi-cast-service:{{ .Values.fastapi.cast.service.port }}/api/v1/casts;
      }
    }