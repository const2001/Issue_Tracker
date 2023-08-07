pipeline {
    agent any

    environment {
        ANSIBLE_HOSTS = 'azurehosts'
        ANSIBLE_REMOTE_USER = 'azureuser'
        ANSIBLE_PLAYBOOK = '~/workspace/ansible-pipeline/anslible_playbook_flask_setup.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone the GitHub repository
                git branch: 'main', url: 'https://github.com/const2001/Issue_Tracker.git'
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                script {
                    // Run the Ansible playbook using the 'ansible-playbook' command
                    def ansibleCmd = "ansible-playbook ${ANSIBLE_PLAYBOOK}"
                    sh ansibleCmd
                }
            }
        }
    }

    post {
        always {
            // Clean up resources, if necessary
        }
    }
}
