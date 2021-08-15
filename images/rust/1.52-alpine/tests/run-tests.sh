#!/bin/sh

set -e

echo "[INFO] Run tests"

echo '[TEST] Print out uname' && \
    uname -a

echo '[TEST] Check rust version' && \
    rustc --version

echo '[TEST] Check cargo version' && \
    cargo version
