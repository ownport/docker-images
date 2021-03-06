# Transmission Docker images

## How to run transmission-daemon
```sh
transmission-daemon --foreground --config-dir /etc/transmission-daemon
```

## How to run docker image

settings.json
```json
{
    "incomplete-dir": "/transmission/incomplete",
    "incomplete-dir-enabled": true,
    "download-dir": "/transmission/downloads",
    "rpc-enabled": true
}
```

```sh
mkdir -p etc/ downloads/ incomplete/

docker run -ti --rm \
    --name transmission-server \
    -v $(pwd)/etc:/etc/transmission \
    -v $(pwd)/downloads:/transmission/downloads \
    -v $(pwd)/incomplete:/transmission/incomplete \
    registry.gitlab.com/ownport/docker-images/transmission:3.0-alpine \
    transmission-daemon --foreground --config-dir /etc/transmission
```
