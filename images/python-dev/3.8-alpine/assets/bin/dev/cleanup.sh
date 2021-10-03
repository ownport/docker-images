#!/bin/sh

set -e


remove_cache_and_egg_files() {

    echo "[INFO] Cleaning cache files" && \
    	find . -name "__pycache__" -type d -prune -exec rm -rf "{}" \;

    echo "[INFO] Cleaning files: *.egg-info" && \
    	find . -name "*.egg-info" -type d -prune -exec rm -rf "{}" \;
}

remove_build_dirs() {

    echo "[INFO] Cleaning build directories" && \
    	rm -rf build dist
}

remove_coverage_reports() {

    echo "[INFO] Cleaning coverage files" && \
    	rm -rf .coverage.* 
}


case ${1} in
    help)
        echo 'Available options:'
        echo ' help         - Displays the help'
        echo ' pre-clean    - Code cleanup before starting project testing or building'
        echo ' post-clean   - Code cleanup after starting project testing or building'
        ;;
    pre-cleanup)
        echo "[INFO] Starting pre-cleanup"
 
        remove_cache_and_egg_files
        remove_build_dirs
        remove_coverage_reports
        ;;

    post-cleanup)
        echo "[INFO] Starting post-cleanup"
        
        remove_cache_and_egg_files
        remove_coverage_reports
        ;;

    *)
        if [ ! "$@" ]; then
            echo "[WARNING] No cleanup mode specified, use help for more details" 
        else
            exec "$@"
        fi
        ;;
esac 




