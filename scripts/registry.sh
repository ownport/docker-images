#!/bin/sh

GITLAB_PROJECT="ownport/docker-images"

URL_REPO_LIST="https://gitlab.com/api/v4/projects/${GITLAB_PROJECT}/registry/repositories"
URL_PROJECT_IDS="https://gitlab.com/api/v4/projects/"

list_projects() {

    curl --header "PRIVATE-TOKEN: ${CU_JOB_TOKEN}" ${URL_PROJECT_IDS}
}

list_repos() {

    curl --header "PRIVATE-TOKEN: ${CU_JOB_TOKEN}" ${URL_REPO_LIST}

}

$@
