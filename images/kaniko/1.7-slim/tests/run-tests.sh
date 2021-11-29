#!/bin/sh

set -e

echo "[INFO] Run tests"

echo '[TEST] Print out Kaniko version' && \
    /kaniko/executor version
