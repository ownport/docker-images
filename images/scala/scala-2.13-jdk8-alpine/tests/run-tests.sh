#!/bin/sh

set -e

echo "[INFO] Run tests"

echo '[TEST] Print out uname' && \
    uname -a

echo '[TEST] Check java version' && \
    java -version

echo '[TEST] Check javac version' && \
    javac -version

echo "[TEST] Check scala version" && \
    scala --version 

echo "[TEST] Check scalac version" && \
    scalac --version
