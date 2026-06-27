pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        BASE_URL = "${params.BASE_URL}"
        PYTHONIOENCODING = 'UTF-8'
        HEADLESS = 'false'
    }

    parameters {
        string(name: 'BASE_URL', defaultValue: 'http://localhost:3001', description: 'Application base URL')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m pip install --upgrade pip
                            python3 -m pip install -r requirements.txt
                            python3 -m playwright install chromium
                            npm install
                        '''
                    } else {
                        bat '''
                            python -m pip install --upgrade pip
                            python -m pip install -r requirements.txt
                            python -m playwright install chromium
                            npm install
                        '''
                    }
                }
            }
        }

        stage('Run Playwright Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            export DISPLAY=:99
                            Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &
                            sleep 2
                            python3 -m pytest tests/test_signup_login.py -v --headed
                        '''
                    } else {
                        bat '''
                            python -m pytest tests/test_signup_login.py -v --headed
                        '''
                    }
                }
            }
        }

        stage('Generate Allure HTML Report') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'npm run allure:report'
                    } else {
                        bat 'npm run allure:report'
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/html/allure-report/**', allowEmptyArchive: true

            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports/html/allure-report',
                reportFiles: 'index.html',
                reportName: 'Allure HTML Report'
            ])

            junit testResults: 'reports/junit/results.xml', allowEmptyResults: true
        }

        success {
            echo 'Tests completed successfully.'
            echo "Allure HTML report: ${env.WORKSPACE}/reports/html/allure-report/index.html"
        }

        failure {
            echo 'Tests failed. Check console output and archived Allure HTML report.'
        }
    }
}
