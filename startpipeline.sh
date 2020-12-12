#!/bin/bash


#echo "My Build url is ----- $BUILD_URL"

echo "START DATETIME is $(date)"

start_time=$(date)

template2='{
    "productname" : "oscar",
    "productversion" : "1.1",
    "projectname":"django-oscar-project-test-travis-ci",
    "environment":"Dev",
    "projectowner":"Deepa Krishna",
    "repositoryurl":"https://github.com/deepakrishnapro/django-oscar",
    "url": "abc",
    "commitid": "5123",
    "jobid": "1",
    "starttime": '$start_time'
}'

echo "$template2"


http_response=$(curl -i \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-w "%{http_code}" \
-X POST --data "$template2" --url http://ec2-54-189-234-66.us-west-2.compute.amazonaws.com:8001/pipeline/start)

statuscode=$(echo "$http_response" |  grep HTTP |  awk '{print $2}')

if [ $statuscode -eq 200 ]; then
	echo "Server returned: Success"
    http_response=(${http_response[@]}) # convert to array
    code=${http_response[-1]} # get last element (last line)
    export PIPELINE_ID=${code%???}
    echo "PIPELINE_ID = ${code%???}"
    #echo $PIPELINE_ID > /var/lib/jenkins/envVars.properties
    #echo $PIPELINE_ID

else
    echo "Server did not return HTTP 200 OK"
fi
