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
                script {
                    echo "Current directory after checkout:"
                    sh 'pwd'
                }
            }
        }

        stage('Build Docker Images') {
            parallel {
                stage('Build cast-service Image') {
                    steps {
                        script {
                            echo "Current directory before building cast-service image:"
                            sh 'pwd'
                            docker.build("didiiiw/jen:cast-service-latest", "-f cast-service/Dockerfile ./cast-service")
                        }
                    }
                }
                stage('Build movie-service Image') {
                    steps {
                        script {
                            echo "Current directory before building movie-service image:"
                            sh 'pwd'
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
                            echo "Current directory before pushing cast-service image:"
                            sh 'pwd'
                            docker.withRegistry('https://index.docker.io/v1/', 'dhub') {
                                docker.image("didiiiw/jen:cast-service-latest").push()
                            }
                        }
                    }
                }
                stage('Push movie-service Image') {
                    steps {
                        script {
                            echo "Current directory before pushing movie-service image:"
                            sh 'pwd'
                            docker.withRegistry('https://index.docker.io/v1/', 'dhub') {
                                docker.image("didiiiw/jen:movie-service-latest").push()
                            }
                        }
                    }
                }
            }
        }

        stage('Deploy to Dev') {
            steps {
                script {
                    echo "Current directory before deploying to Dev:"
                    sh 'pwd'
                    sh 'mkdir -p ~/.kube && cat "$KUBECONFIG_FILE" > ~/.kube/config'
                    sh """
                        helm upgrade --install chart-dev --namespace dev \
                        -f charts/chart-dev/values.yaml \
                        -f charts/chart-dev/values-secret.yaml
                    """
                }
            }
        }

        stage('Deploy to QA') {
            steps {
                script {
                    echo "Current directory before deploying to QA:"
                    sh 'pwd'
                    sh 'mkdir -p ~/.kube && cat "$KUBECONFIG_FILE" > ~/.kube/config'
                    sh """
                        helm install chart-qa --namespace qa \
                        -f charts/chart-qa/values.yaml \
                        -f charts/chart-qa/values-secret.yaml
                    """
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                script {
                    echo "Current directory before deploying to Staging:"
                    sh 'pwd'
                    sh 'mkdir -p ~/.kube && cat "$KUBECONFIG_FILE" > ~/.kube/config'
                    sh """
                        helm install chart-staging --namespace staging \
                        -f charts/chart-staging/values.yaml \
                        -f charts/chart-staging/values-secret.yaml
                    """
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
                    echo "Current directory before deploying to Production:"
                    sh 'pwd'
                    sh 'mkdir -p ~/.kube && cat "$KUBECONFIG_FILE" > ~/.kube/config'
                    sh """
                        helm install chart-prod --namespace prod \
                        -f charts/chart-prod/values.yaml \
                        -f charts/chart-prod/values-secret.yaml
                    """
                }
            }
        }
    }
}
