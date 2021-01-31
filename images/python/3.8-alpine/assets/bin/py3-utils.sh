#!/bin/sh

set -eu

OPTION=${1:-help}

cleanup_cache_files() {

    PY3_PATH=${1:-}

    echo "[INFO] Cleaning cache files" && \
        find ${PY3_PATH} -path '*/__pycache__/*' -delete
        find ${PY3_PATH} -type d -name '__pycache__' -delete
}

case ${OPTION} in
    help)
        shift
        cat << EOM
Usage: py3-utils.sh <option> [arguments]
Available options:'
    install     - install python package(-s) via pip'
        argumens:
            <packages>:     the list of python packages for install
    cleanup     - cleanup'
EOM
        ;;
    install)
        shift
        echo "[INFO] Installing python packages: $@"
        pip3 install --disable-pip-version-check --no-build-isolation --no-cache-dir $@
        ;;
    cleanup)
        echo "[INFO] Cleaning up python cache files"
        cleanup_cache_files /usr/lib/python3.8/
        ;;
    *)
        if [ ! "$@" ]; then
            echo "[WARNING] No arguments specified, use help for more details" 
        else
            exec "$@"
        fi
        ;;
esac 