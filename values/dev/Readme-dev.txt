------

HELM dev

Changer de namespace :
sudo kubectl config set-context $(kubectl config current-context) --namespace=dev

helm install helm-dev-deployment . --namespace dev -f  ./values/dev/values-fastapi-cast.yaml -f ./values/dev/values-fastapi-movie.yaml
 -f ./values/dev/values-nginx.yaml -f ./values/dev/values-postgres-cast.yaml -f ./values/dev/values-postgres-movie.yaml
 -f ./values/dev/values-secret.yaml -f ./values/dev/values-secret.yaml

helm delete helm-dev-deployment --namespace dev


helm dependency update .


-------------------------