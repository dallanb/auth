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
            when {
                expression { env.BRANCH_NAME == 'qaw' || env.BRANCH_NAME == 'prod'}
            }
            steps {
                slackSend (color: '#0000FF', message: "STARTED: Building Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' ")
                script {
                    dockerImageName = registry + ":$BRANCH_NAME"
                    try {
                        docker.image(dockerImageName).pull()
                    } catch (Exception e) {
                        echo 'This image does not exist'
                    }
//                     sh "docker buildx create --name jenkinsbuilder"
                    sh "docker buildx use jenkinsbuilder"
                    sh "docker buildx build -f build/Dockerfile.$BRANCH_NAME -t $dockerImageName --cache-from $dockerImageName --platform linux/amd64 --load ."
                }
            }
        }
        stage('Test') {
            when {
                expression { env.BRANCH_NAME == 'qaw'}
            }
            steps {
                slackSend (color: '#0000FF', message: "Testing Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' ")
                script {
                    try {
                        sh "docker build -f build/Dockerfile.test --cache-from $dockerImageName -t $registry:test ."
                        sh "docker-compose -f docker-compose.test.yaml up -d"
                        sh "bash bin/test.sh"
                        sh "docker cp app:/home/app/tests.xml ."
                        sh "docker cp app:/home/app/coverage.xml ."
                    } finally {
                        sh "docker-compose -f docker-compose.test.yaml down -v"
                        sh "docker image rm $registry:test"
                    }
                }
            }
            post {
                always {
                    script {
                        testSummary = junit testResults: 'tests.xml'
                        cobertura coberturaReportFile: 'coverage.xml', enableNewApi: true
                    }
                    slackSend (
                       color: '#FFFF00',
                       message: "TEST SUMMARY - Passed: ${testSummary.passCount}, Failures: ${testSummary.failCount}, Skipped: ${testSummary.skipCount}"
                    )
                    slackSend (
                       color: '#FFA500',
                       message: "COVERAGE SUMMARY - Report generated at ${env.BUILD_URL}cobertura"
                    )
                }
            }
        }
        stage('Deploy') {
            when {
                expression { env.BRANCH_NAME == 'qaw' || env.BRANCH_NAME == 'prod'}
            }
            steps {
                slackSend (color: '#0000FF', message: "STARTED: Deploying Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' ")
                script {
                    docker.withRegistry( '', registryCredential ) {
                        sh "docker buildx ls"
                        sh "docker buildx create --name jenkinsbuilder"
                        sh "docker buildx use jenkinsbuilder"
                        sh "docker buildx build -f build/Dockerfile.$BRANCH_NAME -t $dockerImageName --cache-from $dockerImageName --platform linux/amd64,linux/arm64 --push ."
                    }
                }
            }
        }
        stage('Clean') {
            when {
                expression { env.BRANCH_NAME == 'qaw' || env.BRANCH_NAME == 'prod'}
            }
            steps {
                slackSend (color: '#0000FF', message: "STARTED: Cleaning Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' ")
                script {
                    sh "docker image prune -f"
                }
            }
        }
        stage('Recreate') {
            when {
                expression { env.BRANCH_NAME == 'qaw' || env.BRANCH_NAME == 'prod'}
            }
            steps {
                slackSend (color: '#0000FF', message: "STARTED: Recreating Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' ")
                script {
                    httpRequest url: 'http://10.0.0.200:10001/hooks/redeploy', contentType: 'APPLICATION_JSON', httpMode: 'POST', requestBody: """
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
    post {
        success {
          slackSend (color: '#00FF00', message: "SUCCESSFUL: Completed Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }

        failure {
          slackSend (color: '#FF0000', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }
    }
}
