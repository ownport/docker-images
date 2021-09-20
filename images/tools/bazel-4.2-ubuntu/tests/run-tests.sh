#!/bin/sh

set -e

echo "[INFO] Run tests"

echo '[TEST] Print out bazel version' && \
    bazel -version
