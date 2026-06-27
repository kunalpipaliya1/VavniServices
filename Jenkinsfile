pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    triggers {
        cron('H 9 * * *')
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

        stage('Clean Old Reports') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -c "from generate_allure_report import cleanup_report_session; cleanup_report_session()"
                        '''
                    } else {
                        bat '''
                            python -c "from generate_allure_report import cleanup_report_session; cleanup_report_session()"
                        '''
                    }
                }
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
            echo 'Scheduled Playwright tests completed successfully.'
            echo "Allure HTML report: ${env.WORKSPACE}/reports/html/allure-report/index.html"
        }

        failure {
            echo 'Scheduled Playwright tests failed. Check console output and archived Allure HTML report.'
        }
    }
}
