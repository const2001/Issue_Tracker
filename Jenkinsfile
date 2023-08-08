pipeline {
    agent any


    stages {
        stage('Clone') {
            steps {
                // Clean up the workspace before starting the build
                deleteDir()

                // Clone the GitHub repository
                       git branch: 'main', url: 'https://github.com/const2001/Issue_Tracker.git'

                     
            }
            
        }

        // stage('Copy project to vm') {
        //     steps {
        //        sh '''
        //             scp -r ~/workspace/flask_vm_docker_setup azureuser@20.0.161.2:/var/www/flask_app

        //         ''' 
                     
        //     }
            
        // }

        stage('Run Ansible Playbook') {
            steps {
                sh '''
                    cd ~/workspace/ansible-pipeline/
                    ansible-playbook anslible_playbook_flask_setup.yml

                '''  
             
                }
            }
        }
    

    
}
