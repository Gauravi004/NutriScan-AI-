pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running app...'
                sh 'python app.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy step (will improve later)...'
            }
        }
    }
}
