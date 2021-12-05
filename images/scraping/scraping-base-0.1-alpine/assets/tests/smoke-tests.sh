#!/bin/sh

echo "[TEST] Getting jq version" && \
    jq --version

echo "[TEST] Getting pytest version" && \
    pytest --version
