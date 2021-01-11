#!/bin/sh

set -eu

SPARK_VERSION=3.0.0
HADOOP_VERSION=2.7
SPARK_DOWNLOAD_URL=https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Preparation
deploy-utils.sh update

deploy-utils.sh install "bash python3"
deploy-utils.sh install-build-deps "wget"

echo "[INFO] Installing Apache Spark" && \
    mkdir -p /tmp/spark &&
    wget --progress=dot:giga ${SPARK_DOWNLOAD_URL} -O /tmp/spark.tgz && \
    tar -xzf /tmp/spark.tgz -C /tmp && \
    mv /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    echo -n "export PATH=\$PATH:/opt/spark/bin" >> ~/.bashrc

# Cleanup procedure
deploy-utils.sh cleanup
