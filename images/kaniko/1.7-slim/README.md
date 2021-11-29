# Kaniko

Build Container Images 

The image `kaniko:1.7-slim` is customized for building docker image for [ownport/docker-images GitLab repo](https://gitlab.com/ownport/docker-images/)

## Customization

- `/kaniko/update-docker-config.sh`: the shell script updates docker config with GitLab CI/CD creds

## References

- https://github.com/GoogleContainerTools/kaniko
- https://docs.gitlab.com/ee/ci/docker/using_kaniko.html

### Dockerfiles

- Dockerfile:latest
  - https://github.com/GoogleContainerTools/kaniko/blob/master/deploy/Dockerfile
- Dockerfile:debug
  - https://github.com/GoogleContainerTools/kaniko/blob/master/deploy/Dockerfile_debug
- Dockerfile:slim
  - https://github.com/GoogleContainerTools/kaniko/blob/master/deploy/Dockerfile_slim
- Dockerfile:warmer
  - https://github.com/GoogleContainerTools/kaniko/blob/master/deploy/Dockerfile_warmer
