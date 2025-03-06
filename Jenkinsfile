pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t your-dockerhub-username/accident-app:latest .'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'dockerhub-credentials']) {
                    sh 'docker push your-dockerhub-username/accident-app:latest'
                }
            }
        }
    }
    post {
        success {
            emailext(
                subject: 'Deployment Successful',
                body: 'The application has been deployed successfully!',
                to: 'admin@example.com'
            )
        }
    }
}
