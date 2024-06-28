pipeline {
    environment {
        DOCKER_ID = 'jhtyl13r'
        DOCKER_TAG = "v.${BUILD_ID}.0"
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
                    sh '''
                    docker rm -f jenkins-movie-fastapi || true
                    docker build -t $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG -f build/movie-fastapi/Dockerfile .
                    docker push $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG
                    sleep 6
                    '''
                }
            }
        }

        stage('Docker Build for cast-fastapi') {
            steps {
                script {
                    sh '''
                    docker rm -f jenkins-cast-fastapi || true
                    docker build -t $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG -f build/cast-fastapi/Dockerfile .
                    docker push $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG
                    sleep 6
                    '''
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
                    // Install chart
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    cat $KUBECONFIG > .kube/config
                    cp ${CHART_DIR}/${VALUES_FILE} values.yml
                    cp ${CHART_DIR}/${VALUES_SECRET_FILE} values-secret.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install ${CHART_NAME} ${CHART_DIR} --values=values.yml --values=values-secret.yml --namespace ${NAMESPACE}
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
                    // Install chart
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    cat $KUBECONFIG > .kube/config
                    cp ${CHART_DIR}/${VALUES_FILE} values.yml
                    cp ${CHART_DIR}/${VALUES_SECRET_FILE} values-secret.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install ${CHART_NAME} ${CHART_DIR} --values=values.yml --values=values-secret.yml --namespace ${NAMESPACE}
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
                    // Install chart
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    cat $KUBECONFIG > .kube/config
                    cp ${CHART_DIR}/${VALUES_FILE} values.yml
                    cp ${CHART_DIR}/${VALUES_SECRET_FILE} values-secret.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install ${CHART_NAME} ${CHART_DIR} --values=values.yml --values=values-secret.yml --namespace ${NAMESPACE}
                    '''
                }
            }
        }

        stage('Deploy to Production') {
            when {
                beforeAgent true
                branch 'main'
                expression { currentBuild.result == 'SUCCESS' && currentBuild.previousBuild.result == 'SUCCESS' && params.DEPLOY_TO_PROD == 'yes' }
            }
            environment {
                VALUES_FILE = 'charts/chart-prod/values.yaml'
                VALUES_SECRET_FILE = 'charts/chart-prod/values-secret.yaml'
                NAMESPACE = 'prod'
                CHART_NAME = 'chart-prod'
                CHART_DIR = 'charts/chart-prod'
            }
            steps {
                script {
                    // Install chart
                    sh '''
                    rm -Rf .kube
                    mkdir .kube
                    cat $KUBECONFIG > .kube/config
                    cp ${CHART_DIR}/${VALUES_FILE} values.yml
                    cp ${CHART_DIR}/${VALUES_SECRET_FILE} values-secret.yml
                    cat values.yml
                    sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                    helm upgrade --install ${CHART_NAME} ${CHART_DIR} --values=values.yml --values=values-secret.yml --namespace ${NAMESPACE}
                    '''
                }
            }
        }
    }
}
