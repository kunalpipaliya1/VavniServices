pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }

    triggers {
        cron('H 9 * * *')
        pollSCM('H/15 * * * *')
    }

    environment {
        BASE_URL = "${params.BASE_URL}"
        PYTHONIOENCODING = 'UTF-8'
        HEADLESS = 'false'
        REPORTS_DIR = "${WORKSPACE}/reports"
        ALLURE_HTML_REPORT = "${WORKSPACE}/reports/html/allure-report/index.html"
    }

    parameters {
        string(
            name: 'BASE_URL',
            defaultValue: 'http://localhost:3001',
            description: 'Application base URL'
        )
        choice(
            name: 'BROWSER',
            choices: ['chromium'],
            description: 'Browser to run Playwright tests'
        )
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
                        sh 'python3 -c "from generate_allure_report import cleanup_report_session; cleanup_report_session()"'
                    } else {
                        bat 'call jenkins\\run-py.bat -c "from generate_allure_report import cleanup_report_session; cleanup_report_session()"'
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
                            python3 -m pip install playwright pytest pytest-playwright allure-pytest
                            python3 -m playwright install chromium
                            npm install allure-commandline --save-dev
                        '''
                    } else {
                        bat '''
                            call jenkins\\install-deps.bat
                        '''
                    }
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 - <<'PY'
import os
import sys
import urllib.request

base_url = os.environ.get("BASE_URL", "http://localhost:3001")
for path in ("/login", "/register"):
    url = f"{base_url}{path}"
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            print(f"{url} -> {response.status}")
    except Exception as error:
        print(f"{url} is not reachable: {error}")
        sys.exit(1)
PY
                        '''
                    } else {
                        bat '''
                            call jenkins\\run-py.bat -c "import os,sys,urllib.request; base=os.environ.get('BASE_URL','http://localhost:3001');
for path in ['/login','/register']:
 url=base+path
 try:
  r=urllib.request.urlopen(url,timeout=20); print(url,'->',r.status)
 except Exception as e:
  print(url,'is not reachable:',e); sys.exit(1)"
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
                        bat 'call jenkins\\run-py.bat -m pytest tests/test_signup_login.py -v --headed'
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/html/allure-report/**', allowEmptyArchive: true
            archiveArtifacts artifacts: 'reports/junit/results.xml', allowEmptyArchive: true

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
            echo "Jenkins build successful."
            echo "Allure HTML report: ${ALLURE_HTML_REPORT}"
        }

        failure {
            echo 'Jenkins build failed. Review console logs, JUnit, and Allure HTML report.'
        }
    }
}
