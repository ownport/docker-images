#!/bin/sh

set -e

echo '[TEST] Print out uname' && \
    uname -a

echo '[TEST] Check python' && \
    python3 --version

# echo '[TEST] Check pip3' && \
#     pip3 --version
