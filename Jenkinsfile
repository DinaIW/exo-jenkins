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

        stage('Deploy to Dev') {
            environment {
                VALUES_FILE = 'charts/chart-dev/values.yaml'
                VALUES_SECRET_FILE = 'charts/chart-dev/values-secret.yaml'
                NAMESPACE = 'dev'
                CHART_NAME = 'chart-dev'
                CHART_DIR = 'charts/chart-dev'
            }
            steps {
                script {
                    sh '''
                    mkdir -p ~/.kube && cp ${KUBECONFIG_FILE} ~/.kube/config
                    cp ${VALUES_FILE} values.yaml
                    cp ${VALUES_SECRET_FILE} values-secret.yaml
                    helm upgrade --install ${CHART_NAME} ${CHART_DIR} \
                    --values=values.yaml \
                    --values=values-secret.yaml \
                    --namespace ${NAMESPACE} \
                    --wait \
                    --set image.repository=didiiiw/jen,image.tag=${DOCKER_TAG}
                    '''
                }
            }
        }

        stage('Deploy to QA') {
            environment {
                VALUES_FILE = 'charts/chart-qa/values.yaml'
                VALUES_SECRET_FILE = 'charts/chart-qa/values-secret.yaml'
                NAMESPACE = 'qa'
                CHART_NAME = 'chart-qa'
                CHART_DIR = 'charts/chart-qa'
            }
            steps {
                script {
                    sh '''
                    mkdir -p ~/.kube && cp ${KUBECONFIG_FILE} ~/.kube/config
                    cp ${VALUES_FILE} values.yaml
                    cp ${VALUES_SECRET_FILE} values-secret.yaml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yaml
                    helm upgrade --install ${CHART_NAME} ${CHART_DIR} \
                    --values=values.yaml \
                    --values=values-secret.yaml \
                    --namespace ${NAMESPACE} \
                    --wait \
                    --set image.repository=didiiiw/jen,image.tag=${DOCKER_TAG}
                    '''
                }
            }
        }

        stage('Deploy to Staging') {
            environment {
                VALUES_FILE = 'charts/chart-staging/values.yaml'
                VALUES_SECRET_FILE = 'charts/chart-staging/values-secret.yaml'
                NAMESPACE = 'staging'
                CHART_NAME = 'chart-staging'
                CHART_DIR = 'charts/chart-staging'
            }
            steps {
                script {
                    sh '''
                    mkdir -p ~/.kube && cp ${KUBECONFIG_FILE} ~/.kube/config
                    cp ${VALUES_FILE} values.yaml
                    cp ${VALUES_SECRET_FILE} values-secret.yaml
                    helm upgrade --install ${CHART_NAME} ${CHART_DIR} \
                    --values=values.yaml \
                    --values=values-secret.yaml \
                    --namespace ${NAMESPACE} \
                    --wait \
                    --set image.repository=didiiiw/jen,image.tag=${DOCKER_TAG}
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
                    helm upgrade --install chart-prod charts/chart-prod \
                    --values=values.yaml \
                    --values=values-secret.yaml \
                    --namespace prod \
                    --wait \
                    --set image.repository=didiiiw/jen,image.tag=${DOCKER_TAG}
                    '''
                }
            }
        }
    }
}
