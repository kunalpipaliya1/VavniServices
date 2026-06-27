pipelineJob('VavniServices-Playwright') {
    description('Scheduled Playwright signup/login tests with Allure HTML reporting.')

    parameters {
        stringParam('BASE_URL', 'http://localhost:3001', 'Application base URL')
        choiceParam('BROWSER', ['chromium'], 'Browser to run Playwright tests')
    }

    triggers {
        cron('H 9 * * *')
        scm('H/15 * * * *')
    }

    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/kunalpipaliya1/VavniServices.git')
                    }
                    branch('*/main')
                }
            }
            scriptPath('Jenkinsfile')
        }
    }
}
