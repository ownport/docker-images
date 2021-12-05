#!/bin/sh

echo "[INFO] Run smoke tests"

echo "[TEST] Getting xsh version" && \
    zsh --version

echo "[TEST] Getting jq version" && \
    jq --version

# echo "[TEST] Getting pytest version" && \
#     pytest --version
