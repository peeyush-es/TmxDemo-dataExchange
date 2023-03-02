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
                sh "sudo docker build --rm --no-cache -t tmxDemo-dataexchange-cron-es:r1 ." 
                }
            }   
        stage("tagging imges"){       //25.00 time stamp
            steps{
                sh  "sudo docker tag tmxDemo-dataexchange-cron-es:r1 $registry/tmxDemo-dataexchange-cron-es:r1 "
                }
            }
        stage("remove old docker image"){
            steps{
                sh  "sudo docker image remove tmxDemo-dataexchange-cron-es:r1"
                }
            }
        stage("image push"){
            steps{                    // account name/image name: version of the tah     
                sh "sudo docker push $registry/tmxDemo-dataexchange-cron-es:r1"  
                }
            }  
        stage("deploying images in DEV ENV"){
            steps{                    // account name/image name: version of the tah     
                sh "sudo docker rm -f tmxDemo-dataexchange-cron-es"
                sh "sudo docker run -d  --name tmxDemo-dataexchange-cron-es $registry/tmxDemo-dataexchange-cron-es:r1"  
            }
        }
    }   
}
