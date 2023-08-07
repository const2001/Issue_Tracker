pipeline {
    agent any

    environment {
        ANSIBLE_HOSTS = 'azurehosts'
        ANSIBLE_REMOTE_USER = 'azureuser'
        ANSIBLE_PLAYBOOK = '~/workspace/ansible-pipeline/anslible_playbook_flask_setup.yml'
    }

    stages {
        stage('Preparation') {
            steps {
                // Clean up the workspace before starting the build
                deleteDir()

                // Clone the GitHub repository
                       git branch: 'main', url: 'https://github.com/const2001/Issue_Tracker.git'
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                script {
                    try {
                        // Run the Ansible playbook using the 'ansible-playbook' command
                          def ansibleCmd = "ansible-playbook -i ${ANSIBLE_HOSTS}, -u ${ANSIBLE_REMOTE_USER} ${ANSIBLE_PLAYBOOK}"
                        sh ansibleCmd
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
        }
    }

    
}
