#!/bin/sh

set -e

/usr/local/bin/dev/cleanup.sh pre-cleanup

# In case of using local PyPi server use pip3 with the next options:
#   --trusted-host pypi-server
#   --extra-index-url http://pypi-server:8080/simple/

pip3 install -e . && pytest 

/usr/local/bin/dev/cleanup.sh post-cleanup

