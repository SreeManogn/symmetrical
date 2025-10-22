pipeline { 
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image..."
               bat "docker build -t movie-reviewapp:v1 ."
            }
        }

        stage('Docker Login') {
            steps {
                echo "Logging into Docker Hub..."
                bat 'docker login -u shivaji108 -p Kaveri@1729'
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
               bat 'docker tag movie-reviewapp:v1 shivaji108/sample:kuberimg2' 
                bat 'docker push shivaji108/sample:kuberimg2'
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
            echo "Deployment successful! Movie Review App is now live on Kubernetes."
        }
        failure {
            echo "Deployment failed. Check Jenkins logs for errors."
        }
    }
}
