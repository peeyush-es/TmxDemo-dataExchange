pipeline {
    agent any  
      environment{
        registry= "dev.exactspace.co"
      }
    stages{
        stage("get scm"){
            steps{
                checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[url: 'git@github.com:exact-space/TmxDemo-dataExchange.git']])
            }
        }
        stage("building images"){
            steps{
                sh "sudo docker build --rm --no-cache -t TmxDemo-dataExchange-cron-es:r1 ." 
                }
            }   
        stage("tagging imges"){       //25.00 time stamp
            steps{
                sh  "sudo docker tag TmxDemo-dataExchange-cron-es:r1 $registry/TmxDemo-dataExchange-cron-es:r1 "
                }
            }
        stage("remove old docker image"){
            steps{
                sh  "sudo docker image remove TmxDemo-dataExchange-cron-es:r1"
                }
            }
        stage("image push"){
            steps{                    // account name/image name: version of the tah     
                sh "sudo docker push $registry/TmxDemo-dataExchange-cron-es:r1"  
                }
            }  
        stage("deploying images in DEV ENV"){
            steps{                    // account name/image name: version of the tah     
                sh "sudo docker rm -f TmxDemo-dataExchange-cron-es"
                sh "sudo docker run -d -p 6121:6121 --name TmxDemo-dataExchange-cron-es $registry/TmxDemo-dataExchange-cron-es:r1"  
            }
        }
    }   
}
