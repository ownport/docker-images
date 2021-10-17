#!/bin/sh


GITLAB_PROJECT_ID="23580555"

# URLs
URL_REPO_LIST="https://gitlab.com/api/v4/projects/${GITLAB_PROJECT_ID}/registry/repositories"

list_repos() {

    curl --silent --header "PRIVATE-TOKEN: ${CU_JOB_TOKEN}" \
        ${URL_REPO_LIST}
}

$@
