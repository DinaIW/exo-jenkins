Lancer le chart :
helm install chart-dev --namespace dev ./chart-dev/ -f ./chart-dev/values.yaml -f ./chart-dev/values-secret.yaml
helm uninstall chart-dev -n dev

-----

ENV DEV

- Pas de ingress
- resources limités (request, limits, cpu) a revoir
- Bdd legère (512Mi)
- Bdd de test : movie_db_dev & cast_db_dev

