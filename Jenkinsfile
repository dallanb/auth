pipeline {
    environment {
        githubCredential = 'github'
        container = 'auth'
        registry = "dallanbhatti/auth"
        registryCredential = 'dockerhub'
    }
    agent any
    stages {
        stage('Build') {
            steps {
                slackSend (color: '#0000FF', message: "STARTED: Building Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' ")
                script {
                    dockerImageName = registry + ":$BRANCH_NAME"
                    dockerImage = ''
                    if (env.BRANCH_NAME == 'qaw') {
                        try {
                            docker.image(dockerImageName).pull()
                        } catch (Exception e) {
                            echo 'This image does not exist'
                        }
                        dockerImage = docker.build(dockerImageName, "-f build/Dockerfile.$BRANCH_NAME --cache-from $dockerImageName .")
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                slackSend (color: '#0000FF', message: "STARTED: Deploying Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' ")
                script {
                    if (dockerImage) {
                        docker.withRegistry( '', registryCredential ) {
                            dockerImage.push()
                        }
                    }
                }
            }
        }
        stage('Clean') {
            steps {
                slackSend (color: '#0000FF', message: "STARTED: Cleaning Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' ")
                script {
                    if (dockerImage) {
                        sh "docker image prune -f"
                    }
                }
            }
        }
        stage('Recreate') {
            steps {
                slackSend (color: '#0000FF', message: "STARTED: Recreating Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' ")
                script {
                    if (dockerImage) {
                        httpRequest url: 'http://192.168.0.100:10001/hooks/redeploy', contentType: 'APPLICATION_JSON', httpMode: 'POST', requestBody: """
                            {
                                "project": {
                                    "name": "$container",
                                    "env": "$BRANCH_NAME"
                                }
                            }
                        """
                    }
                }
            }
        }
    }
    post {
        success {
          slackSend (color: '#00FF00', message: "SUCCESSFUL: Completed Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }

        failure {
          slackSend (color: '#FF0000', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }
    }
}