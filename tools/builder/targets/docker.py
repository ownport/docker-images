

import sys
import logging
import subprocess

from pathlib import Path

from builder.fs import pushd
from builder.target import Target

from argparse import ArgumentParser

logger = logging.getLogger(__name__)


# GitLab Docker Registry
GITLAB_DOCKER_REGISTRY="registry.gitlab.com"
# GitLab Group
GITLAB_GROUP="ownport"
# GitLab Project
GITLAB_PROJECT="docker-images"


class DockerCommandException(Exception):
    pass

# Error codes
ERROR_BUILD_DOCKER_IMAGE=1001
ERROR_TEST_DOCKER_IMAGE=1002
ERROR_REMOVE_DOCKER_IMAGE=1003
ERROR_PUBLISH_DOCKER_IMAGE=1004

# The list of supported branches
# SUPPORTED_BRANCHES = ['devel', 'pre-release', 'release']

class Docker:

    def __init__(self, path:Path, branch:str) -> None:

        # if branch.lower() not in SUPPORTED_BRANCHES:
        #     raise RuntimeError(f"Unknown branch name, {branch}. Supported: {SUPPORTED_BRANCHES}")
        self._branch = branch

        if not Path(path).joinpath('Dockerfile').exists():
            raise RuntimeError(f"Dockerfile does not exist in the path, {path}")
        self._target = Target(path)

        target_type = self._target.info.get("type")
        if not target_type and target_type != 'docker_image':
            raise ValueError(f'Target type shall be "docker_image", founded: {target_type}')

        self._docker_image = self._target.info.get("name")
        if not self._docker_image:
            raise ValueError(f'No docker name')

        self._docker_version = self._target.info.get("version")
        if not self._docker_version:
            logger.warning('No docker version, using `latest`')
            self._docker_version = 'latest'

        self._docker_image = "/".join([
                                    GITLAB_DOCKER_REGISTRY, GITLAB_GROUP, 
                                    GITLAB_PROJECT, self._branch, self._docker_image])
        self._docker_image_uri = ':'.join([self._docker_image, self._docker_version])
        

    def _run_command(self, command, errors="strict") -> subprocess.Popen:

        command = ['docker', ] + command
        logger.info(f"Run command: {' '.join(command)}")
        process =  subprocess.Popen(command, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)
        process.communicate()
        if process.returncode != 0:
            raise DockerCommandException() 

    def build(self) -> None:
        ''' build docker image from target
        '''
        logger.info(f'Building docker image for target: {self._target.info}')
        logger.info(f"Docker image: {self._docker_image_uri}")

        # Pull existing docker image
        try:
            docker_command = ['pull', self._docker_image_uri]
            self._run_command(docker_command)
        except DockerCommandException:
            logger.warning(f'Failed to pull docker image, {self._docker_image_uri}')

        # Build docker image
        with pushd(self._target.path):
            try:
                docker_command = ['build', 
                                    '--build-arg', f'BRANCH={self._branch}',
                                    '--cache-from', self._docker_image_uri,
                                    '--tag', self._docker_image_uri, '.']
                self._run_command(docker_command)
            except DockerCommandException:
                logger.error(f'Failed to build docker image, image: {self._docker_image_uri}, tag: {self._docker_image_uri}')
                sys.exit(ERROR_BUILD_DOCKER_IMAGE)

    def test(self) -> None:
        ''' test docker image for target
        '''
        logger.info(f'Testing docker image for target: {self._target.info}')
        logger.info(f"Docker image: {self._docker_image_uri}")

        # Run tests for docker image
        tests_volume_path = f"{self._target.path.absolute().joinpath('tests/')}"
        with pushd(self._target.path):
            try:
                docker_command = ['run', '--rm', 
                                    '-v', f"{tests_volume_path}:/tests", 
                                    self._docker_image_uri,
                                    "/tests/run-tests.sh"]
                self._run_command(docker_command)
            except DockerCommandException:
                logger.error(f'Failed to test docker image, image: {self._docker_image_uri}')
                sys.exit(ERROR_TEST_DOCKER_IMAGE)

    def remove(self) -> None:
        ''' remove docker image for target
        '''
        logger.info(f'Removing docker image for target: {self._target.info}')
        logger.info(f"Docker image: {self._docker_image_uri}")

        try:
            self._run_command(['image', 'rm', self._docker_image_uri])
        except DockerCommandException:
            logger.error(f'Failed to remove docker image, image: {self._docker_image_uri}')
            sys.exit(ERROR_REMOVE_DOCKER_IMAGE)

    def publish(self) -> None:
        ''' Publish docker image for target
        '''
        logger.info(f'Removing docker image for target: {self._target.info} to GitLab Registry: {GITLAB_DOCKER_REGISTRY}')
        logger.info(f"Docker image: {self._docker_image_uri}")

        # Push docker image(-s) to GitLab Docker Registry
        try:
            self._run_command(["push", self._docker_image_uri])
        except DockerCommandException:
            logger.error(f'Failed to publish docker image, image: {self._docker_image_uri}')
            sys.exit(ERROR_PUBLISH_DOCKER_IMAGE)


def add_docker_arguments(parser: ArgumentParser) -> ArgumentParser:

    parser.add_argument('--target-path', type=str, required=True,
                                help='The path to target')
    parser.add_argument('--build', action='store_true', 
                                help='build docker image for target')
    parser.add_argument('--remove', action='store_true', 
                                help='remove docker image for target')
    parser.add_argument('--test', action='store_true', 
                                help='test docker image for target')
    parser.add_argument('--publish', action='store_true', 
                                help='publish docker image for target')
    parser.add_argument('--branch', type=str, required=True, default='test', 
                                help='docker registry branch')
    parser.set_defaults(handler=handle_cli_commands)


def handle_cli_commands(args):

    target_path = args.target_path
    branch = args.branch

    docker = Docker(path=target_path, branch=branch)

    if args.build:
        docker.build()

    elif args.remove:
        docker.remove()

    elif args.test:
        docker.test()

    elif args.publish:
        docker.publish()
