pipeline {
    environment {
        DOCKER_ID = 'jhtyl13r'
        DOCKER_TAG = "v.${BUILD_ID}.0"
        DOCKER_PASS = credentials('DOCKER_HUB_PASS')
        KUBECONFIG = credentials('config')
        NAMESPACES = ['dev', 'qa', 'staging', 'prod']
    }
    agent any

    stages {
        stage('Docker Build and Test') {
            steps {
                script {
                    // Assuming Docker build and test steps for movie-fastapi and cast-fastapi are done similarly
                    
                    // Docker build and test for movie-fastapi
                    sh '''
                    docker rm -f jenkins-movie-fastapi || true
                    docker build -t $DOCKER_ID/movie-fastapi:$DOCKER_TAG -f build/movie-fastapi/Dockerfile .
                    sleep 6
                    curl localhost
                    '''

                    // Docker build and test for cast-fastapi
                    sh '''
                    docker rm -f jenkins-cast-fastapi || true
                    docker build -t $DOCKER_ID/cast-fastapi:$DOCKER_TAG -f build/cast-fastapi/Dockerfile .
                    sleep 6
                    curl localhost
                    '''
                }
            }
        }

        stage('Deployment to Dev') {
            environment {
                VALUES_FILE = 'charts/chart-dev/movie-fastapi/values-dev.yaml'
            }
            steps {
                script {
                    def chartName = 'chart-dev'
                    def namespace = 'dev'
                    def chartDir = "charts/chart-dev"
                    def valuesFile = "charts/chart-dev/values.yaml"
                    def valuesSecretFile = "charts/chart-dev/values-secret.yaml"

                    // Check if chart is already installed
                    def chartInstalled = sh(returnStdout: true, script: "helm list -n ${namespace} | grep ${chartName}").trim()
                    if (chartInstalled) {
                        // Uninstall chart
                        sh "helm uninstall ${chartName} -n ${namespace}"
                    }

                    // Install chart
                    sh "helm install ${chartName} ${chartDir} -f ${valuesFile} -f ${valuesSecretFile} --namespace ${namespace}"
                }
            }
        }

        stage('Deploy to QA') {
            when {
                beforeAgent true
                branch 'main'
                expression { currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    def chartName = 'chart-qa'
                    def namespace = 'qa'
                    def chartDir = "charts/chart-qa"
                    def valuesFile = "charts/chart-qa/values.yaml"
                    def valuesSecretFile = "charts/chart-qa/values-secret.yaml"

                    // Check if chart is already installed
                    def chartInstalled = sh(returnStdout: true, script: "helm list -n ${namespace} | grep ${chartName}").trim()
                    if (chartInstalled) {
                        // Uninstall chart
                        sh "helm uninstall ${chartName} -n ${namespace}"
                    }

                    // Install chart
                    sh "helm install ${chartName} ${chartDir} -f ${valuesFile} -f ${valuesSecretFile} --namespace ${namespace}"
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                beforeAgent true
                branch 'main'
                expression { currentBuild.result == 'SUCCESS' && currentBuild.previousBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    def chartName = 'chart-staging'
                    def namespace = 'staging'
                    def chartDir = "charts/chart-staging"
                    def valuesFile = "charts/chart-staging/values.yaml"
                    def valuesSecretFile = "charts/chart-staging/values-secret.yaml"

                    // Check if chart is already installed
                    def chartInstalled = sh(returnStdout: true, script: "helm list -n ${namespace} | grep ${chartName}").trim()
                    if (chartInstalled) {
                        // Uninstall chart
                        sh "helm uninstall ${chartName} -n ${namespace}"
                    }

                    // Install chart
                    sh "helm install ${chartName} ${chartDir} -f ${valuesFile} -f ${valuesSecretFile} --namespace ${namespace}"
                }
            }
        }

        stage('Deploy to Production') {
            when {
                beforeAgent true
                branch 'main'
                expression { currentBuild.result == 'SUCCESS' && currentBuild.previousBuild.result == 'SUCCESS' && params.DEPLOY_TO_PROD == 'yes' }
            }
            steps {
                script {
                    def chartName = 'chart-prod'
                    def namespace = 'prod'
                    def chartDir = "charts/chart-prod"
                    
