#!/bin/sh

set -e

echo "[INFO] Run tests"

echo "[TEST] Check pytest" && \
    pytest --version
