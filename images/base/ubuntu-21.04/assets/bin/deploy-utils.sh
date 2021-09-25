#!/bin/bash

set -eu

export DEBIAN_FRONTEND=noninteractive

install_build_deps() {

    PACKAGES=$@
    for pkg in $@
    do 
        echo -n "$pkg" > /tmp/.build-deps
        apt install -y --no-install-recommends $pkg 
    done
}

remove_build_deps() {

    [ -f /tmp/.build-deps ] && {
        for pkg in `cat /tmp/.build-deps`
        do 
            apt purge -y --auto-remove $pkg
        done
    } || {
        echo "[WARNING] No .build-deps file, removing build deps was skipped"
    }
}

case ${1} in
    help)
        echo 'Available options:'
        echo ' update               - update Ubuntu packages'
        echo ' install              - install packages'
        echo ' install-build-deps   - install build deps'
        echo ' cleanup              - cleanup'
        ;;
    update)
        echo "[INFO] Update apt index" && \
            apt update
        ;;
    install)
        shift
        echo "[INFO] Installing the packages: $@" && \
            apt install -y --no-install-recommends $@
        ;;
    install-build-deps)
        shift
        echo "[INFO] Installing the packages: $@" && \
            install_build_deps $@
        ;;
    cleanup)
        echo "[INFO] Removing build deps packages" && \
            remove_build_deps

        echo "[INFO] Clearing out the local repository of retrieved package files" && \
            apt clean
        
        echo "[INFO] Removing apt index" && \
            rm -rf \
                /var/cache/* \
                /var/lib/apt/lists/* \
                /tmp/*
        ;;
    *)
        if [ ! "$@" ]; then
            echo "[WARNING] No arguments specified, use help for more details" 
        else
            exec "$@"
        fi
        ;;
esac 

