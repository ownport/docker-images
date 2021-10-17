#!/bin/sh


GITLAB_PROJECT="ownport/docker-images"

URL_REPO_LIST="https://gitlab.com/api/v4/projects/${GITLAB_PROJECT}/registry/repositories"
URL_PROJECT_IDS="https://gitlab.com/api/v4/projects/ownport/"

list_projects() {

    curl --silent --header "PRIVATE-TOKEN: ${CU_JOB_TOKEN}" \
        ${URL_PROJECT_IDS} | jq .
}

list_repos() {

    curl --silent --header "PRIVATE-TOKEN: ${CU_JOB_TOKEN}" \
        ${URL_REPO_LIST}
}

$@
