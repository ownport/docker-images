#!/bin/sh

set -e

echo "[INFO] Run tests"

# =================================================
# Versions
#
echo "[TEST] Check zsh version" && \
    zsh --version

echo "[TEST] Check make version" && \
    make --version

echo "[TEST] Check git version" && \
    git version

echo "[TEST] Check jq version" && \
    jq --version

echo "[TEST] Check twine version" && \
    twine --version

echo "[TEST] Check pip-tools version" && \
    pip-compile --version && \
    pip-sync --version

echo "[TEST] Check pre-commit version" && \
    pre-commit --version

echo "[TEST] Check pylint version" && \
    pylint --version

echo "[TEST] Check pytest version" && \
    pytest --version

echo "[TEST] Check coverage version" && \
    coverage --version

echo "[TEST] Check dev scripts" && {
    SCRIPTS="cleanup.sh release.sh run-pytest.sh publish.sh"
    for script in ${SCRIPTS}; do
        DEV_SCRIPT="/usr/local/bin/dev/${script}"
        echo "[INFO] Checking ${DEV_SCRIPT}"
        [ ! -f ${DEV_SCRIPT} ] && { 
            echo "[ERROR] Missing ${DEV_SCRIPT}"
            exit 1
        }
    done
}

echo "[INFO] Tests were completed"
