pipeline {
    agent any
    stages {
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t votingapp:v1 .'
            }
        }
        stage('Docker login') {
            steps {
                bat 'docker login -u 22251a1257it258 -p Manogna18@gnits'
            }
        }
        stage('Push Docker Image to Docker hub') {
            steps {
                echo "pushing docker image"
                bat 'docker tag votingapp:v1 22251a1257it258/symmetry:kuberimg1'
                bat 'docker push 22251a1257it258/symmetry:kuberimg1'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }
}
