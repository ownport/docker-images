
import logging
import argparse

from buildtools.git import add_git_arguments
from buildtools.target import add_target_argumens
from buildtools.targets.docker import add_docker_arguments


logger = logging.getLogger(__name__)


def run_cli():

    parser = argparse.ArgumentParser('buildtools')

    parser.add_argument('-l', '--log-level',
                        default='INFO',
                        help='Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL')

    subparsers = parser.add_subparsers()

    # Git commands
    git_parser = subparsers.add_parser('git', help='Git commands')
    git_parser = add_git_arguments(git_parser)

    # Target commands
    target_parser = subparsers.add_parser('target', help='Target commands')
    target_parser = add_target_argumens(target_parser)

    # Docker commands
    docker_parser = subparsers.add_parser('docker', help='Docker commads')
    docker_parser = add_docker_arguments(docker_parser)

    # Main
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level,
                            format="%(asctime)s.%(msecs)03d (%(name)s) [%(levelname)s] %(message)s",
                            datefmt='%Y-%m-%dT%H:%M:%S')

    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()