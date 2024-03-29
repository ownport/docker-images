
import os
from posixpath import abspath
import sys
import json
import base64
import logging
import subprocess

from pathlib import Path
from argparse import ArgumentParser

from builder.fs import pushd
from builder.target import Target
from builder.settings import Settings

logger = logging.getLogger(__name__)


class KanikoImageCommandException(Exception):
    pass

# Error codes
ERROR_ENV_CONFIGURATION=1001
ERROR_BUILD_KANIKO_IMAGE=1002
ERROR_BUILD_CONFIG=1003


class KanikoImage:

    def __init__(self, path:Path, branch:str, settings:dict={}) -> None:

        self._branch = branch
        self._settings = settings

        if not Path(path).joinpath('Dockerfile').exists():
            raise RuntimeError(f"Dockerfile does not exist in the path, {path}")
        self._target = Target(path)
        self._target.info['path'] = path

        target_type = self._target.info.get("type")
        if not target_type and target_type != 'kaniko-image':
            raise ValueError(f'Target type shall be "kaniko-image", founded: {target_type}')

        self._image_name = self._target.info.get("name")
        if not self._image_name:
            raise ValueError(f'No image name')

        self._image_version = self._target.info.get("version")
        if not self._image_version:
            logger.warning('No image version, using `latest`')
            self._image_version = 'latest'

        self._image_uri = "/".join([
                                    self._settings.get('registry', None),
                                    self._branch, 
                                    self._image_name])
        self._image_uri = ':'.join([self._image_uri, self._image_version])

        logger.info(f'Image URI: {self._image_uri}')

        os.environ['DOCKER_CONFIG'] = '/kaniko/.docker/'
        os.environ['SSL_CERT_DIR'] = '/kaniko/ssl/certs'


    def _run_command(self, command, errors="strict") -> subprocess.Popen:

        kaniko_env = os.environ.copy()

        command = ['executor', ] + command
        logger.info(f"Current directory: {os.path.abspath(os.curdir)}")
        logger.info(f"Run command: {' '.join(command)}")
        process =  subprocess.Popen(command, 
                                    stdin=subprocess.PIPE, 
                                    stdout=sys.stdout, 
                                    stderr=sys.stderr,
                                    env=kaniko_env)
        process.communicate()
        if process.returncode != 0:
            raise KanikoImageCommandException() 

    def build(self) -> None:
        ''' build docker image from target
        '''
        logger.info(f'Building docker image for target: {self._target.info}')
        logger.info(f"Docker image: {self._image_uri}")

        # Build docker image with kaniko executor
        with pushd(self._target.path):
            try:
                # target_path = os.path.abspath(self._target.info.get('path'))
                kaniko_command = [
                    '--context', '.',
                    '--dockerfile', 'Dockerfile',
                    '--build-arg', f'BRANCH={self._branch}',
                    '--cache',
                    '--destination', self._image_uri ]
                self._run_command(kaniko_command)
            except KanikoImageCommandException:
                logger.error(f'Failed to build docker image, image: {self._image_uri}')
                sys.exit(ERROR_BUILD_KANIKO_IMAGE)

    @staticmethod
    def update_config(settings:dict) -> None:
        ''' Update kaniko configuration 
        '''
        CI_REGISTRY = os.environ.get("CI_REGISTRY")
        CI_REGISTRY_USER = os.environ.get("CI_REGISTRY_USER")
        CI_REGISTRY_PASSWORD = os.environ.get("CI_REGISTRY_PASSWORD")
        if not CI_REGISTRY or not CI_REGISTRY_USER or not CI_REGISTRY_PASSWORD:
            logger.error('Missed one of environment variables: CI_REGISTRY or CI_REGISTRY_USER or CI_REGISTRY_PASSWORD')
            sys.exit(ERROR_ENV_CONFIGURATION)

        config_path = settings.get('config')
        logger.info(f'Kaniko configiration file: {config_path}')
        config_dirname = os.path.dirname(config_path)
        if not Path(config_dirname).exists():
            os.makedirs(config_dirname)

        config_json = { 'auths': {
                f"{CI_REGISTRY}" : { "auth": base64.b64encode(
                                                        f"{CI_REGISTRY_USER}:{CI_REGISTRY_PASSWORD}".encode('ascii')
                ).decode('ascii') }
        }}

        with open(config_path, 'w') as kaniko_config:
            kaniko_config.write("{}\n".format(
                json.dumps(config_json)
            ))


def add_kaniko_arguments(parser: ArgumentParser) -> ArgumentParser:

    parser.add_argument('--target-path', type=str,
                                help='The path to target')
    parser.add_argument('--build', action='store_true', 
                                help='build docker image for target')
    parser.add_argument('--update-config', action='store_true', 
                                help='update kaniko config with registry auth settings')
    parser.add_argument('--branch', type=str, default='test', 
                                help='docker registry branch')
    parser.set_defaults(handler=handle_cli_commands)


def handle_cli_commands(args):

    target_path = args.target_path
    branch = args.branch
    settings = Settings(args.settings)

    if args.update_config:
        KanikoImage.update_config(settings.get('kaniko', default={}))

    elif args.build:
        if not target_path or not branch:
            logger.error("The following arguments are required for build action: --target-path, --branch")
            sys.exit(ERROR_BUILD_CONFIG)

        kaniko = KanikoImage(path=target_path, branch=branch, settings=settings.get('kaniko', {}))
        kaniko.build()
