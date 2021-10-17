#!/bin/sh

GITLAB_PROJECT="docker-images"

URL_REPO_LIST="https://gitlab.example.com/api/v4/projects/${GITLAB_PROJECT}/registry/repositories"

list_repos() {

    curl --header "PRIVATE-TOKEN: ${CU_JOB_TOKEN}" ${URL_REPO_LIST}

}

$@
