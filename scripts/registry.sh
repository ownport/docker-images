#!/bin/sh


GITLAB_PROJECT_ID="23580555"

# URLs
URL_REPO_LIST="https://gitlab.com/api/v4/projects/${GITLAB_PROJECT_ID}/registry/repositories?tags_count=true"

list_repos() {

    GROUP_NAME=${1:-}

    curl --silent --header "PRIVATE-TOKEN: ${CI_JOB_TOKEN}" \
        ${URL_REPO_LIST} | jq . #\
    # jq -c ".[] | select(.name | contains(\"${GROUP_NAME}\"))"
}

delete_repo() {

    REPO_ID=${1:-}
    echo "[INFO] Deleting the repo, id: ${REPO_ID}"
}

$@
