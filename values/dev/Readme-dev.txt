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

helm template ./datascientest
sudo su
kubectl config view --raw > ~/.kube/config
helm install datascientest-chart ./datascientest --values=./datascientest/values.yaml
exit #revenir sur l'utilisateur courant

maj = helm upgrade datascientest-chart ./datascientest --values=./datascientest/values.yaml

kubectl describe deploy datascientest-chart
/

---git

git push -u origin dev