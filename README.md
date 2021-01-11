# docker-images

The collection of docker images. The list of available docker images, [docs/docker-images.md](docs/docker-images.md)

## How to use

### Build docker image

To build docker image use

```sh
./manage.sh build <path to Dockerfile>
```

For example:
```sh
./manage.sh build images/base/alpine-3.12
[INFO] Building image: images/base/alpine-3.12/
...
Successfully tagged ownport/base:3.12-alpine
```

### Run console with a docker image

To run console for specific image
```sh
./manage.sh console <path to Dockerfile>
```

For example:
```sh
./manage.sh console images/base/alpine-3.12
[INFO] Running console for image: images/base/alpine-3.12/
[INFO] The image: ownport/base:3.12-alpine, the container name: base-console
/ # 
```
