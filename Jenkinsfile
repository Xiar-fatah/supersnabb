pipeline {
    agent {
      docker {
        image 'python:3'
      }
    }
    stages {
        stage('Python Version') {
            steps {
                sh """python --version"""
            }
        }
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/test-jenkins']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/Xiar-fatah/supersnabb.git']])
            }
        }
        stage('Install') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh '''pip install virtualenv
                    python3 -m venv supersnabb
                    . supersnabb/bin/activate            
                    pip install -r requirements.txt
                    python -m pytest'''
                }
            }
        }
    }
}
