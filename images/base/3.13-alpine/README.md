# Base image with Alpine

## deploy utils

### /usr/local/bin/deploy-utils.sh update

Update Alpine packages list

### /usr/local/bin/deploy-utils.sh install

Install packages. For example:

```sh
./deploy-utils.sh install "make curl jq"
```

### /usr/local/bin/deploy-utils.sh install-build-deps

Install build dependencies packages. They will be removed as final stage of docker image build. 

For example:
```sh
./deploy-utils.sh install-build-deps "gcc musl-dev"
```

### /usr/local/bin/deploy-utils.sh cleanup

Cleanup procedure: removing packages list, build deps, etc.


