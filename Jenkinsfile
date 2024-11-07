pipeline {
    agent any
    environment {
        APP_DIR = '/home/ec2-user/Stock_Proj_1st_OCT'  // Adjust path as needed
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/DarbhaPreetham/Stock_Proj_1st_OCT.git'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'pytest tests/'  // Adjust test command as needed
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                # Stop current service
                sudo systemctl stop stockapp.service
                
                # Copy new code
                cp -r * $APP_DIR
                
                # Start service
                sudo systemctl start stockapp.service
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Deployment was successful!'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}
