#!/bin/sh

set -e

echo "[INFO] Run tests"

echo '[TEST] Print out uname' && \
    uname -a

echo '[TEST] Check ZSH version' && \
    zsh --version
