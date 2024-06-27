
Lancer le chart :
helm install chart-prod --namespace prod ./chart-prod/ -f ./chart-prod/values.yaml -f ./chart-prod/values-secret.yaml
helm uninstall chart-prod -n prod

ENV QA

-Nouvelle base :
    cast_db_prod
    movie_db_prod

-Nouveau mot de passe plus fort

- Création du ingress laissé en http (cert sera fait en prod)

- augementation des ressources (values.yaml)

- insertion d'une bdd plus conséquente



https://devops.dev-euphony.fr/api/v1/movies/docs#/