pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo 'Installing Python and dependencies...'
                sh '''
                apt-get update
                apt-get install -y python3 python3-pip
                pip3 install --break-system-packages -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running application...'
                sh '''
                python3 app.py
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy stage (will improve later)...'
            }
        }
    }
}
