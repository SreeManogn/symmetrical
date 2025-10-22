pipeline { 
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image..."
               bat "docker build -t devopsapp1:v1 ."
            }
        }

        stage('Docker Login') {
            steps {
                echo "Logging into Docker Hub..."
                bat 'docker login -u 22251a1257it258 -p Manogna18@gnits'
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
               bat 'docker tag devopsapp1:v1 22251a1257it258/devopsapp1:kuberimg3' 
               bat 'docker push 22251a1257it258/devopsapp1:kuberimg3 || exit 0'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying to Kubernetes..."
                bat "kubectl apply -f deployment.yaml --validate=false"
                bat "kubectl apply -f service.yaml"
            }
        }
    }

    post {
        success {
            echo "Deployment successful! "
        }
        failure {
            echo "Deployment failed. Check Jenkins logs for errors."
        }
    }
}
