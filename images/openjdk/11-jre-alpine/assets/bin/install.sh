#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "openjdk11-jre libc6-compat"
echo "[INFO] Creating sym link for ld-linux-x86-64.so.2" && \
    ln -s /lib64/ld-linux-x86-64.so.2 /lib/ld-linux-x86-64.so.2

echo "[WARNING] Creating OpenJDK symlinks (fix Alpine openjdk11-jre package)"

JDK_TOOLS_TO_INSTALL="java keytool pack200 rmid rmiregistry unpack200"

for tool in ${JDK_TOOLS_TO_INSTALL};
do
    [ -L /usr/bin/${tool} ] && {
        rm /usr/bin/${tool}
        ln -s /usr/lib/jvm/default-jvm/bin/${tool} /usr/bin/${tool}
    }
done

# Cleanup procedure
deploy-utils.sh cleanup


