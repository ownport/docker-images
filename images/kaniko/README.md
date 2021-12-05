# Kaniko docker images

## How to build kaniko images locally

to build one of kaniko version run
```sh
./builder docker --target-path images/kaniko/1.6-slim --build
```
or
```sh
./builder docker --target-path images/kaniko/1.7-slim --build
```

login to  registry.gitlab.com
```sh
docker login registry.gitlab.com
```

publish docker image
```sh
./builder docker --target-path images/kaniko/1.6-slim --publish
```
or
```sh
./builder docker --target-path images/kaniko/1.7-slim --publish
```


## References

- https://github.com/GoogleContainerTools/kaniko
