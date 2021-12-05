

import sys
import json
import logging
import subprocess


from builder.command import Command

from argparse import ArgumentParser

logger = logging.getLogger(__name__)


class DockerCommandException(Exception):
    pass


class DockerTools:

    def _get_docker_command(self, args:list) -> list:
        ''' return docker command
        '''
        return ['docker', ] + args

    def _run_command(self, args:list, errors="strict") -> subprocess.Popen:

        command = self._get_docker_command(args)
        logger.info(f"Run command: {' '.join(command)}")
        process =  subprocess.Popen(command, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)
        process.communicate()
        if process.returncode != 0:
            raise DockerCommandException() 
        return process

    def _check_output(self, args, failure_msg=None, errors="strict"):

        command = self._get_docker_command(args)
        logger.debug(f"Run command: {' '.join(command)}")
        process, out, err = Command.invoke(command)
        return Command.cleanse(out)

    def list_containers(self):
        ''' rerurns the list of docker containers
        '''
        containers = list()
        try:
            docker_command = ['container', 'ls', '-a', '--format', '{{json .}}']
            containers = [json.loads(cnt) 
                            for cnt in self._check_output(docker_command).split('\n') if cnt]
        except DockerCommandException:
            logger.warning(f'Failed to get containers list')
        return containers

    def list_images(self):
        ''' rerurns the list of docker images
        '''        
        images = list()
        try:
            docker_command = ['image', 'ls', "--format", '{{json .}}']
            images = [json.loads(img) 
                        for img in self._check_output(docker_command).split('\n') if img]
        except DockerCommandException:
            logger.warning(f'Failed to get images list')
        return images

    def stop_all_containers(self) -> None:
        ''' stop all containers
        '''
        containers = self.list_containers()
        logger.info(f"Stopping of containers: {containers}")
        try:
            for container in containers:
                if container.get('State') in ('running'):
                    docker_command = ['container', 'stop', container.get("ID")]
                    self._run_command(docker_command)
        except DockerCommandException:
            logger.warning(f'Failed to stop container, {container}')
        logger.info("Stopping of containers was completed")

    def remove_exited_containers(self) -> None:
        ''' remove exited containers
        '''
        containers = self.list_containers()
        logger.info(f"Removing of exited containers: {containers}")
        try:
            for container in containers:
                if container.get('State') in ('exited', 'created'):
                    docker_command = ['container', 'rm', container.get("ID")]
                    self._run_command(docker_command)
        except DockerCommandException:
            logger.warning(f'Failed to remove container, {container}')
        logger.info("Removing of exited containers was completed")

    def remove_none_images(self) -> None:
        ''' remove None images
        '''
        images = self.list_images()
        logger.info("Removing of none images")
        try:
            for image in images:
                if image.get('Repository') == '<none>' or image.get('Tag') == '<none>':
                    docker_command = ['image', 'rm', image.get("ID")]
                    self._run_command(docker_command)
        except DockerCommandException:
            logger.warning(f'Failed to remove image, {image}')
        logger.info("Removing of none images was completed")

    def remove_all_images(self) -> None:
        ''' remove all images
        '''
        images = self.list_images()
        logger.info("Removing of all images")
        try:
            for image in images:
                docker_command = ['image', 'rm', image.get("ID")]
                self._run_command(docker_command)
        except DockerCommandException:
            logger.warning(f'Failed to remove image, {image}')
        logger.info("Removing of all images was completed")

    def remove_all_containers(self) -> None:
        ''' remove all containers
        '''
        self.stop_all_containers()
        self.remove_exited_containers()

def add_docker_tools_arguments(parser: ArgumentParser) -> ArgumentParser:

    # Containers
    parser.add_argument('--list-containers', action='store_true', 
                                help='list containers')
    parser.add_argument('--stop-all-containers', action='store_true', 
                                help='stop all containers')
    parser.add_argument('--remove-exited-containers', action='store_true', 
                                help='remove exited containers')
    parser.add_argument('--remove-all-containers', action='store_true', 
                                help='remove all containers')

    # Images
    parser.add_argument('--list-images', action='store_true', 
                                help='list images')
    parser.add_argument('--remove-none-images', action='store_true', 
                                help='remove none images')
    parser.add_argument('--remove-all-images', action='store_true', 
                                help='remove all images')
    parser.set_defaults(handler=handle_cli_commands)


def handle_cli_commands(args):


    docker_tools = DockerTools()

    if args.list_containers:
        print(json.dumps(docker_tools.list_containers()))

    if args.stop_all_containers:
        docker_tools.stop_all_containers()

    if args.remove_exited_containers:
        docker_tools.remove_exited_containers()

    if args.remove_all_containers:
        docker_tools.remove_all_containers()

    if args.list_images:
        print(json.dumps(docker_tools.list_images()))

    if args.remove_none_images:
        docker_tools.remove_exited_containers()
        docker_tools.remove_none_images()

    if args.remove_all_images:
        docker_tools.remove_all_images()
