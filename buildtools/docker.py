

import sys
import logging
import subprocess

from pathlib import Path

from buildtools.fs import pushd
from buildtools.target import Target


logger = logging.getLogger(__name__)


# GitLab Docker Registry
GITLAB_DOCKER_REGISTRY="registry.gitlab.com"
# GitLab Group
GITLAB_GROUP="ownport"
# GitLab Project
GITLAB_PROJECT="docker-images"


class Docker:

    def __init__(self, path:Path, dev_image:bool=False) -> None:

        if not Path(path).joinpath('Dockerfile').exists():
            raise RuntimeError(f"Dockerfile does not exist in the path, {path}")
        self._target = Target(path)
        
        target_type = self._target.info.get("type")
        if not target_type:
            raise ValueError(f'Target type shall be docker, founded: {target_type}')

        self._docker_image = self._target.info.get("docker_image", {}).get("name")
        if not self._docker_image:
            raise ValueError(f'No docker name')

        self._docker_version = self._target.info.get("docker_image", {}).get("version")
        if not self._docker_version:
            logger.warning('No docker version, using `latest`')
            self._docker_version = 'latest'

        self._docker_image = "/".join([GITLAB_DOCKER_REGISTRY, GITLAB_GROUP, GITLAB_PROJECT, self._docker_image])
        self._docker_image_uri = ':'.join([self._docker_image, self._docker_version])
        if dev_image:
            self._docker_image_uri += "-dev"

    def _run_command(self, command, errors="strict") -> subprocess.Popen:

        command = ['docker', ] + command
        logger.info(f"Run command: {' '.join(command)}")
        process =  subprocess.Popen(command, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)
        process.communicate()

    def build(self) -> None:
        ''' build docker image from target
        '''
        logger.info(f'Building docker image for target: {self._target.info}')
        logger.info(f"Docker image: {self._docker_image_uri}")

        # Pull existing docker image
        self._run_command(['pull', self._docker_image_uri])

        # Build docker image
        with pushd(self._target.path):
            self._run_command(['build', 
                                '--cache-from', self._docker_image_uri,
                                '--tag', self._docker_image_uri, '.'])

    def test(self) -> None:
        ''' test docker image for target
        '''
        logger.info(f'Testing docker image for target: {self._target.info}')
        logger.info(f"Docker image: {self._docker_image_uri}")

        # Run tests for docker image
        tests_volume_path = f"{self._target.path.absolute().joinpath('tests/')}"
        with pushd(self._target.path):
            self._run_command(['run', '--rm', 
                                '-v', f"{tests_volume_path}:/tests", 
                                self._docker_image_uri,
                                "/tests/run-tests.sh"])

    def remove(self) -> None:
        ''' remove docker image for target
        '''
        logger.info(f'Removing docker image for target: {self._target.info}')
        logger.info(f"Docker image: {self._docker_image_uri}")

        self._run_command(['image', 'rm', self._docker_image_uri])

    def publish(self) -> None:
        ''' Publish docker image for target
        '''
        logger.info(f'Removing docker image for target: {self._target.info} to GitLab Registry: {GITLAB_DOCKER_REGISTRY}')
        logger.info(f"Docker image: {self._docker_image_uri}")

        # Push docker image(-s) to GitLab Docker Registry
        self._run_command(["push", self._docker_image_uri])
