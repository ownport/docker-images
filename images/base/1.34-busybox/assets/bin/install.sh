#!/bin/sh

set -eu

echo "[INFO] Running smoke tests" && \
    /tmp/assets/tests/smoke-tests.sh
