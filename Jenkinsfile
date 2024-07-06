pipeline {
    agent any

    environment {
        DOCKER_HUB_PASS = credentials('dhub')
        KUBECONFIG_FILE = credentials('kubeconfig-credentials')
        GITHUB_CREDENTIALS = credentials('github-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-credentials', url: 'https://github.com/DinaIW/examjen.git'
            }
        }

        stage('Build Docker Images') {
            parallel {
                stage('Build cast-service Image') {
                    steps {
                        script {
                            docker.build("didiiiw/jen:cast-service-latest", "-f cast-service/Dockerfile ./cast-service")
                        }
                    }
                }
                stage('Build movie-service Image') {
                    steps {
                        script {
                            docker.build("didiiiw/jen:movie-service-latest", "-f movie-service/Dockerfile ./movie-service")
                        }
                    }
                }
            }
        }

        stage('Push Docker Images') {
            parallel {
                stage('Push cast-service Image') {
                    steps {
                        script {
                            docker.withRegistry('https://index.docker.io/v1/', 'dhub') {
                                docker.image("didiiiw/jen:cast-service-latest").push()
                            }
                        }
                    }
                }
                stage('Push movie-service Image') {
                    steps {
                        script {
                            docker.withRegistry('https://index.docker.io/v1/', 'dhub') {
                                docker.image("didiiiw/jen:movie-service-latest").push()
                            }
                        }
                    }
                }
            }
        }

        stage('Package Helm Chart') {
            steps {
                script {
                    sh '''
                    helm package charts/chart-dev -d charts/chart-dev
                    helm package charts/chart-qa -d charts/chart-qa
                    helm package charts/chart-staging -d charts/chart-staging
                    helm package charts/chart-prod -d charts/chart-prod
                    '''
                }
            }
        }

        stage('Deploy to Dev') {
            environment {
                NAMESPACE = 'dev'
                CHART_NAME = 'chart-dev'
                CHART_PACKAGE = 'charts/chart-dev/chart-dev-0.1.0.tgz'
                VALUES_FILE = 'charts/chart-dev/values.yaml'
                VALUES_SECRET_FILE = 'charts/chart-dev/values-secret.yaml'
            }
            steps {
                script {
                    sh '''
                    mkdir -p ~/.kube && cp ${KUBECONFIG_FILE} ~/.kube/config
                    cp ${VALUES_FILE} values.yaml
                    cp ${VALUES_SECRET_FILE} values-secret.yaml
                    helm upgrade --install ${CHART_NAME} ${CHART_PACKAGE} \
                    --namespace ${NAMESPACE} \
                    --values=values.yaml \
                    --values=values-secret.yaml \
                    --set image.repository=didiiiw/jen,image.tag=cast-service-latest \
                    --wait
                    '''
                }
            }
        }

        stage('Deploy to QA') {
            environment {
                NAMESPACE = 'qa'
                CHART_NAME = 'chart-qa'
                CHART_PACKAGE = 'charts/chart-qa/chart-qa-0.1.0.tgz'
                VALUES_FILE = 'charts/chart-qa/values.yaml'
                VALUES_SECRET_FILE = 'charts/chart-qa/values-secret.yaml'
            }
            steps {
                script {
                    sh '''
                    mkdir -p ~/.kube && cp ${KUBECONFIG_FILE} ~/.kube/config
                    cp ${VALUES_FILE} values.yaml
                    cp ${VALUES_SECRET_FILE} values-secret.yaml
                    helm upgrade --install ${CHART_NAME} ${CHART_PACKAGE} \
                    --namespace ${NAMESPACE} \
                    --values=values.yaml \
                    --values=values-secret.yaml \
                    --wait
                    '''
                }
            }
        }

        stage('Deploy to Staging') {
            environment {
                NAMESPACE = 'staging'
                CHART_NAME = 'chart-staging'
                CHART_PACKAGE = 'charts/chart-staging/chart-staging-0.1.0.tgz'
                VALUES_FILE = 'charts/chart-staging/values.yaml'
                VALUES_SECRET_FILE = 'charts/chart-staging/values-secret.yaml'
            }
            steps {
                script {
                    sh '''
                    mkdir -p ~/.kube && cp ${KUBECONFIG_FILE} ~/.kube/config
                    cp ${VALUES_FILE} values.yaml
                    cp ${VALUES_SECRET_FILE} values-secret.yaml
                    helm upgrade --install ${CHART_NAME} ${CHART_PACKAGE} \
                    --namespace ${NAMESPACE} \
                    --values=values.yaml \
                    --values=values-secret.yaml \
                    --wait
                    '''
                }
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'master'
            }
            steps {
                input message: 'Deploy to Production?', ok: 'Deploy'
                script {
                    sh '''
                    mkdir -p ~/.kube && cp ${KUBECONFIG_FILE} ~/.kube/config
                    cp ${VALUES_FILE} values.yaml
                    cp ${VALUES_SECRET_FILE} values-secret.yaml
                    helm upgrade --install chart-prod charts/chart-prod-0.1.0.tgz \
                    --namespace prod \
                    --values=values.yaml \
                    --values=values-secret.yaml \
                    --wait
                    '''
                }
            }
        }
    }
}
