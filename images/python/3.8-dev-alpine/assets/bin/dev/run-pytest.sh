#!/bin/bash

set -e

/usr/sbin/dev/cleanup.sh pre-cleanup

# In case of using local PyPi server use pip3 with the next options:
#   --trusted-host pypi-server
#   --extra-index-url http://pypi-server:8080/simple/

pip3 install -e . && \
    PYTHONDONTWRITEBYTECODE=1 pytest \
    --cov=eventsflow \
    -p no:cacheprovider \
    --junitxml=report.xml \
    --cov-report=term-missing \
    --cov-config=.coveragerc

/usr/sbin/dev/cleanup.sh post-cleanup

