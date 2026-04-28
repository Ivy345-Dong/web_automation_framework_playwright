pipeline {
    agent any

    tools {
        python 'Python3'  // 确保 Jenkins 配置了名为 "Python3" 的 Python 工具
    }

    environment {
        // 设置环境变量
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                echo 'Cleaning workspace...'
                // 删除旧的测试结果目录（相当于 PowerShell 的 Remove-Item）
                sh 'rm -rf allure-results report || true'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip install pytest pytest-xdist allure-pytest -q'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests with pytest...'
                // 运行 pytest 测试，使用 3 个并行进程，无头模式
                sh 'pytest -n 3 --headless -v'
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Generating Allure report...'
                // 生成 Allure 报告
                sh 'allure generate ./allure-results -o ./report --clean'
            }
        }

        stage('Publish Allure Report') {
            steps {
                echo 'Publishing Allure report...'
                // 发布 Allure 报告到 Jenkins
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: './allure-results']]
                ])
            }
        }
    }

    post {
        always {
            echo 'Test pipeline finished'
        }
        success {
            echo 'All tests passed!'
        }
        failure {
            echo 'Some tests failed!'
        }
    }
}