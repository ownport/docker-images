#!/bin/sh

set -eu

echo "[INFO] Install deploy-utils script" && \
        mv /tmp/assets/bin/deploy-utils.sh /usr/local/bin/ && \
    
echo "[INFO] Running smoke tests" && \
    /tmp/assets/tests/smoke-tests.sh
