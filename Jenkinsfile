pipeline {
    agent any

    environment {
        IMAGE_NAME = "aryanraj47/task-manager"
    }

    stages {
        stage('Clone') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER .'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm $IMAGE_NAME:$BUILD_NUMBER pytest test_app.py -v'
            }
        }

        stage('Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker tag $IMAGE_NAME:$BUILD_NUMBER $IMAGE_NAME:latest'
                    sh 'docker push $IMAGE_NAME:latest'
                }
            }
        }

        stage('Deploy to K8s') {
            steps {
                sh 'kubectl apply -f k8s/'
                sh 'kubectl set image deployment/task-manager task-manager=$IMAGE_NAME:latest'
            }
        }
    }

    post {
        success { echo 'Pipeline succeeded!' }
        failure { echo 'Pipeline failed.' }
    }
}
