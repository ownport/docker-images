#!/bin/sh

set -eu

cleanup_cache_files() {

    PY3_PATH=${1:-}

    echo "[INFO] Cleaning cache files" && \
        find ${PY3_PATH} -path '*/__pycache__/*' -delete
        find ${PY3_PATH} -type d -name '__pycache__' -delete
}

case ${1} in
    help)
        echo 'Available options:'
        echo ' install              - install python package(-s) via pip'
        echo ' cleanup              - cleanup'
        ;;
    install)
        shift
        pip3 install --disable-pip-version-check --no-build-isolation --no-cache-dir $@
        ;;
    cleanup)
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