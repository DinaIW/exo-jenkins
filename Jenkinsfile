        stage('Deploy to Production') {
            environment {
                VALUES_FILE = 'charts/chart-prod/values.yaml'
                VALUES_SECRET_FILE = 'charts/chart-prod/values-secret.yaml'
                NAMESPACE = 'prod'
                CHART_NAME = 'chart-prod'
                CHART_DIR = 'charts/chart-prod'
            }
            steps {
                script {
                    // Demander une confirmation avant de déployer en production
                    timeout(time: 15, unit: 'MINUTES') {
                        def userInput = input(
                            message: 'Êtes-vous sûr de vouloir déployer en production ?',
                            ok: 'Déployer',
                            parameters: [
                                [$class: 'BooleanParameterDefinition', name: 'confirm', defaultValue: false]
                            ]
                        )
                        if (!userInput.confirm) {
                            error('Déploiement en production annulé.')
                        }
                    }

                    // Vérifier si le chart est déjà installé
                    def chartInstalled = sh(returnStdout: true, script: "helm ls -n ${NAMESPACE} | grep ${CHART_NAME}").trim()
                    if (chartInstalled) {
                        // Mise à niveau du chart
                        sh '''
                        rm -Rf .kube
                        mkdir .kube
                        cp $KUBECONFIG .kube/config
                        cp ${VALUES_FILE} values.yml
                        cp ${VALUES_SECRET_FILE} values-secret.yml
                        sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                        helm upgrade ${CHART_NAME} ${CHART_DIR} \
                        --values=values.yml \
                        --values=values-secret.yml \
                        --namespace ${NAMESPACE} \
                        --wait \
                        --set fastapi_movie.tag=${DOCKER_TAG} \
                        --set fastapi_cast.tag=${DOCKER_TAG}
                        '''
                    } else {
                        // Installation du chart
                        sh '''
                        rm -Rf .kube
                        mkdir .kube
                        cp $KUBECONFIG .kube/config
                        cp ${VALUES_FILE} values.yml
                        cp ${VALUES_SECRET_FILE} values-secret.yml
                        sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                        helm install ${CHART_NAME} ${CHART_DIR} \
                        --values=values.yml \
                        --values=values-secret.yml \
                        --namespace ${NAMESPACE} \
                        --wait \
                        --set fastapi_movie.tag=${DOCKER_TAG} \
                        --set fastapi_cast.tag=${DOCKER_TAG}
                        '''
                    }
                }
            }
        }
