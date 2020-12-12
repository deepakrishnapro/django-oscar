#!/bin/bash

#echo "My Build url is ----- $BUILD_URL"

echo "START DATETIME is $(date +%s)"

template2='{
    "productname" : "oscar",
    "productversion" : "1.1",
    "projectname":"'$TRAVIS_JOB_NAME'",
    "environment":"Dev",
    "projectowner":"Deepa Krishna",
    "repositoryurl":"https://github.com/deepakrishnapro/django-oscar",
    "url": "'$TRAVIS_JOB_WEB_URL'",
    "commitid": "5123",
    "jobid": "'$TRAVIS_JOB_NUMBER'",
    "starttime": '$start_time'
}'

echo "$template2"
