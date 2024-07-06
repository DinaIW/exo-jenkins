
Lancer le chart :
helm install chart-staging --namespace staging ./chart-staging/ -f ./chart-staging/values.yaml -f ./chart-staging/values-secret.yaml
helm uninstall chart-staging -n staging

ENV QA

-Nouvelle base :
    cast_db_staging
    movie_db_staging

-Nouveau mot de passe plus fort

- Création du ingress en http (cert sera fait en prod)

- augementation des ressources (values.yaml)

- insertion d'une bdd plus conséquente

