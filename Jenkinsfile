pipeline {
    agent any

    environment {
        ANSIBLE_PLAYBOOK = '~/workspace/ansible-pipeline/anslible_playbook_flask_setup.yml'
    }

    stages {
        stage('Preparation') {
            steps {
                // Clean up the workspace before starting the build
                deleteDir()

                // Clone the GitHub repository
                git branch: 'main', url: "${env.GITHUB_URL}/${env.GITHUB_REPOSITORY}.git"
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                script {
                    try {
                        // Run the Ansible playbook using the 'ansible-playbook' command
                        def ansibleCmd = "ansible-playbook ${ANSIBLE_PLAYBOOK}"
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
