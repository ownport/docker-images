
import logging
import argparse

from builder.git import add_git_arguments
from builder.target import add_target_argumens
from builder.docker_tools import add_docker_tools_arguments
from builder.targets.docker import add_docker_arguments
from builder.targets.kaniko import add_kaniko_arguments


logger = logging.getLogger(__name__)


def run_cli():

    parser = argparse.ArgumentParser('builder')
    subparsers = parser.add_subparsers()

    # Common parser
    common_parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-l', '--log-level',
                        default='INFO',
                        help='Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    parser.add_argument('--settings', type=str, default='.builder.yml',
                        help='The path to builder settings file, default: ./builder.yml')
    
    # Git commands
    add_git_arguments(
        subparsers.add_parser('git', help='Git commands'))

    # Target commands
    add_target_argumens(
        subparsers.add_parser('target', help='Target commands'))

    # Docker commands
    add_docker_arguments(
        subparsers.add_parser('docker', help='Docker commads'))

    # Docker Tools commands
    add_docker_tools_arguments(
        subparsers.add_parser('docker-tools', help='Docker Tools commads'))

    # Kaniko commands
    add_kaniko_arguments(
        subparsers.add_parser('kaniko', help='Kaniko commands'))

    # Main
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level,
                            format="%(asctime)s.%(msecs)03d (%(name)s) [%(levelname)s] %(message)s",
                            datefmt='%Y-%m-%dT%H:%M:%S')

    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()