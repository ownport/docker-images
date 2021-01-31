#!/bin/sh

set -e

echo "[INFO] Run tests"

echo "[TEST] Check if vscode user exist" && \
    id vscode

echo "[INFO] Tests were completed"
