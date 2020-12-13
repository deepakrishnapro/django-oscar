#!/bin/bash

#echo "My Build url is ----- $BUILD_URL"

echo "START DATETIME is $(date +%s)"

start_time=$(date +%s)

job_id=${TRAVIS_JOB_NUMBER%.*}

template2='{
    "productname" : "oscar-from-travis",
    "productversion" : "1.1",
    "projectname":"'$TRAVIS_JOB_NAME'",
    "environment":"Dev",
    "projectowner":"Deepa Krishna",
    "repositoryurl":"https://github.com/deepakrishnapro/django-oscar",
    "url": "'$TRAVIS_JOB_WEB_URL'",
    "commitid": "5123",
    "jobid": "'$job_id'",
    "starttime": '$start_time'
}'

echo "$template2"

http_response=$(curl -i \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-w "%{http_code}" \
-X POST --data "$template2" --url http://ec2-54-189-234-66.us-west-2.compute.amazonaws.com:8001/pipeline/start)

statuscode=$(echo "$http_response" |  grep HTTP |  awk '{print $2}')

if [ "$statuscode" -eq 200 ]; then
    echo "Server returned: Success"
    http_response=(${http_response[@]}) # convert to array
    code=${http_response[-1]} # get last element (last line)
    export PIPELINE_ID=${code%???}
    echo "PIPELINE_ID = ${code%???}"
    #echo $PIPELINE_ID > /var/lib/jenkins/envVars.properties
    echo "$PIPELINE_ID"
else
    echo "Server did not return HTTP 200 OK"
fi
