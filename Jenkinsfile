pipeline {
    agent any
    parameters {
        choice(name: 'DEPLOY_TO_PROD', choices: ['yes', 'no'], description: 'Deploy to production after successful staging deployment?')
    }
    stages {
        stage('Deploy to Dev') {
            steps {
                script {
                    def chartName = 'chart-dev'
                    def namespace = 'dev'
                    def valuesFile = "charts/chart-dev/values.yaml"
                    def valuesSecretFile = "charts/chart-dev/values-secret.yaml"
                    def chartDir = "charts/chart-dev"

                    // Check if chart is already installed
                    def chartInstalled = sh(returnStdout: true, script: "helm list -n ${namespace} | grep ${chartName}").trim()
                    if (chartInstalled) {
                        // Uninstall chart
                        sh "helm uninstall ${chartName} -n ${namespace}"
                    }

                    // Install chart with two values files
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
                    def valuesFile = "charts/chart-qa/values.yaml"
                    def valuesSecretFile = "charts/chart-qa/values-secret.yaml"
                    def chartDir = "charts/chart-qa"

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
                    def valuesFile = "charts/chart-staging/values.yaml"
                    def valuesSecretFile = "charts/chart-staging/values-secret.yaml"
                    def chartDir = "charts/chart-staging"

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
                    def valuesFile = "charts/chart-prod/values.yaml"
                    def valuesSecretFile = "charts/chart-prod/values-secret.yaml"
                    def chartDir = "charts/chart-prod"

                    // Check if chart is already installed
                    def chartInstalled = sh(returnStdout: true, script: "helm list -n ${namespace} | grep ${chartName}").trim()
                    if (chartInstalled) {
                        // Uninstall chart
                        sh "helm uninstall ${chartName} -n ${namespace}"
                    }

                    // Ask for confirmation before deploying to production
                    input message: 'Are you sure you want to deploy to production?'

                    // Install chart
                    sh "helm install ${chartName} ${chartDir} -f ${valuesFile} -f ${valuesSecretFile} --namespace ${namespace}"
                }
            }
        }
    }
}
