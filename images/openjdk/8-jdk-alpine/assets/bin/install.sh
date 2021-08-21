#!/bin/sh

set -eu

# removing extra files
cleanup() {

    echo "[INFO] Cleaning extra files" && \
        rm -rf \
            /usr/share/X11 \
            /usr/share/fonts \
            /usr/share/fontconfig
}

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "openjdk8 libc6-compat"
echo "[INFO] Creating sym link for ld-linux-x86-64.so.2" && \
    ln -s /lib64/ld-linux-x86-64.so.2 /lib/ld-linux-x86-64.so.2

echo "[WARNING] Creating OpenJDK symlinks (fix Alpine openjdk8 package)"

JDK_TOOLS="jaotc jar jarsigner java javac javadoc javap jcmd jdb jdeprscan"
JDK_TOOLS="${JDK_TOOLS} jdeps jexec jexec-bin jfr jhsdb jimage jinfo jjs jlink"
JDK_TOOLS="${JDK_TOOLS} jmap jmod jps jrunscript jshell jstack jstat jstatd"
JDK_TOOLS="${JDK_TOOLS} keytool pack200 rmic rmid rmiregistry serialver unpack200"

for tool in ${JDK_TOOLS};
do
    [ -L /usr/bin/${tool} ] && {
        rm /usr/bin/${tool}
        ln -s /usr/lib/jvm/default-jvm/bin/${tool} /usr/bin/${tool}
    }
done

# Cleanup procedure
cleanup
deploy-utils.sh cleanup
