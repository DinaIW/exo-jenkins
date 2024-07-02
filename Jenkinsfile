// TO DO
/*
Factoriser le code (Build Docker)
Utiliser des variables pour le stockage des chemins d'accès.
Ajouter des notifications de l'état du pipeline
Test automatisés
Automatiser le changement de version dans les différent Chart Helm
*/


pipeline {
    environment {
        DOCKER_ID = 'jhtyl13r'
        DOCKER_TAG = "v.${env.BUILD_ID}.0"
        DOCKER_IMAGE_MOVIE = 'movie-fastapi'
        DOCKER_IMAGE_CAST = 'cast-fastapi'
        DOCKER_PASS = credentials('DOCKER_HUB_PASS')
        KUBECONFIG = credentials('config')
    }
    agent any

    stages {
        stage('Docker Build for movie-fastapi') {
            steps {
                script {
                    // Vérifier si le Dockerfile a changé
                    sh 'git diff --exit-code HEAD^ HEAD build/movie-service/Dockerfile'
                    if (currentBuild.result == 'SUCCESS') {
                        sh '''
                        docker build -t $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG -f build/movie-service/Dockerfile .
                        docker login -u $DOCKER_ID -p $DOCKER_PASS
                        docker push $DOCKER_ID/$DOCKER_IMAGE_MOVIE:${DOCKER_TAG}
                        sleep 6
                        '''
                    } else {
                        echo 'Aucun changement dans le Dockerfile, pas de build ni de push de l\'image'
                    }
                }
            }
        }

        stage('Docker Build for cast-fastapi') {
            steps {
                script {
                    // Vérifier si le Dockerfile a changé
                    sh 'git diff --exit-code HEAD^ HEAD build/cast-service/Dockerfile'
                    if (currentBuild.result == 'SUCCESS') {
                        sh '''
                        docker build -t $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG -f build/cast-service/Dockerfile .
                        docker login -u $DOCKER_ID -p $DOCKER_PASS
                        docker push $DOCKER_ID/$DOCKER_IMAGE_CAST:${DOCKER_TAG}
                        sleep 6
                        '''
                    } else {
                        echo 'Aucun changement dans le Dockerfile, pas de build ni de push de l\'image'
                    }
                }
            }
        }

        stage('Deployment to Dev') {
            environment {
                VALUES_FILE = 'charts/chart-dev/values.yaml'
                VALUES_SECRET_FILE = 'charts/chart-dev/values-secret.yaml'
                NAMESPACE = 'dev'
                CHART_NAME = 'chart-dev'
                CHART_DIR = 'charts/chart-dev'
            }
            steps {
                script {
                    // Installation du Chart Dev
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    cp $KUBECONFIG .kube/config
                    cp ${VALUES_FILE} values.yml
                    cp ${VALUES_SECRET_FILE} values-secret.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install ${CHART_NAME} ${CHART_DIR} \
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


        stage('Deployment to qa') {
            environment {
                VALUES_FILE = 'charts/chart-qa/values.yaml'
                VALUES_SECRET_FILE = 'charts/chart-qa/values-secret.yaml'
                NAMESPACE = 'qa'
                CHART_NAME = 'chart-qa'
                CHART_DIR = 'charts/chart-qa'
            }
            steps {
                script {
                    // Installation du Chart QA
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    cp $KUBECONFIG .kube/config
                    cp ${VALUES_FILE} values.yml
                    cp ${VALUES_SECRET_FILE} values-secret.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install ${CHART_NAME} ${CHART_DIR} \
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

        stage('Deployment to staging') {
            environment {
                VALUES_FILE = 'charts/chart-staging/values.yaml'
                VALUES_SECRET_FILE = 'charts/chart-staging/values-secret.yaml'
                NAMESPACE = 'staging'
                CHART_NAME = 'chart-staging'
                CHART_DIR = 'charts/chart-staging'
            }
            steps {
                script {
                    // Installation du Chart Staging
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    cp $KUBECONFIG .kube/config
                    cp ${VALUES_FILE} values.yml
                    cp ${VALUES_SECRET_FILE} values-secret.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install ${CHART_NAME} ${CHART_DIR} \
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
                    timeout(time: 1, unit: 'HOURS') {
                        def userInput = input(
                            message: 'Êtes-vous sûr de vouloir déployer en production ?',
                            ok: 'Déployer',
                            parameters: [
                                [$class: 'BooleanParameterDefinition', name: 'confirm', defaultValue: false]
                            ]
                        )
                        if (userInput == false) {
                            error('Déploiement en production annulé.')
                        } else if (params.DEPLOY_TO_PROD == 'yes') {
                            // Installation du Chart Prod
                            sh '''
                            rm -Rf .kube
                            mkdir .kube
                            cp $KUBECONFIG .kube/config
                            cp ${VALUES_FILE} values.yml
                            cp ${VALUES_SECRET_FILE} values-secret.yml
                            sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                            helm upgrade --install ${CHART_NAME} ${CHART_DIR} \
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
        }

    }
}
