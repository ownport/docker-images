#!/bin/sh

set -eu

get_reg() {

    REG_SHA256="ade837fc5224acd8c34732bf54a94f579b47851cc6a7fd5899a98386b782e228"
    REG_VERSION="0.16.1"

    curl -fSL \
        https://github.com/genuinetools/reg/releases/download/v${REG_VERSION}/reg-linux-amd64 \
        -o "/usr/local/bin/reg" && \
    echo "${REG_SHA256}  /usr/local/bin/reg" | sha256sum -c - && \
	chmod a+x /usr/local/bin/reg
}

echo "[INFO] Installing console tools" && \
    deploy-utils.sh install "curl jq"

echo "[INFO] Installing Docker registry v2 command line client" && \
    get_reg

echo "[INFO] Running smoke tests" && \
    /tmp/assets/tests/smoke-tests.sh

echo "[INFO] Cleaning" && \
    deploy-utils.sh cleanup
