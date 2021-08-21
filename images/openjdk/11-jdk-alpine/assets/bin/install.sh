#!/bin/sh

set -eu

# removing extra files
cleanup() {

    echo "[INFO] Cleaning extra files" && \
        rm -rf \
            /usr/share/X11 \
            /usr/lib/jvm/java-11-openjdk/man \
            /usr/lib/jvm/java-11-openjdk/demo \
            /usr/lib/jvm/java-11-openjdk/jmods/java.desktop.* \
            /usr/lib/jvm/java-11-openjdk/jmods/jdk.unsupported.desktop.jmod
}


# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "openjdk11 libc6-compat"
echo "[INFO] Creating sym link for ld-linux-x86-64.so.2" && \
    ln -s /lib64/ld-linux-x86-64.so.2 /lib/ld-linux-x86-64.so.2

echo "[WARNING] Creating OpenJDK symlinks (fix Alpine openjdk11 package)"

JDK_TOOLS="jaotc jar jarsigner java javac javadoc javap jcmd jconsole jdb jdeprscan"
JDK_TOOLS="${JDK_TOOLS} jdeps jfr jimage jinfo jjs jlink jmap jmod jps jrunscript"
JDK_TOOLS="${JDK_TOOLS} jshell jstack jstat jstatd keytool pack200 rmic rmid rmiregistry"
JDK_TOOLS="${JDK_TOOLS} serialver unpack200"

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




