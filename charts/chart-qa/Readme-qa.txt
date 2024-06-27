Lancer le chart :
helm install chart-qa --namespace qa ./chart-qa/ -f ./chart-qa/values.yaml -f ./chart-qa/values-secret.yaml
helm uninstall chart-qa -n qa


ENV QA

-Nouvelle base :
    cast_db_qa
    movie_db_qa

-Considérant que dans l'exercisse il n'y ai pas besoin de feedback extrene je n'ajouterai pas d'ingress ici

-Intégration d'une base de donnée plus fournis

-Création de fichier script automatisé pour tester l'application. (Dans jenkins ?)
