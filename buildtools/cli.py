
import string
import logging
import argparse

from pathlib import Path

from buildtools.git import Git
from buildtools.docker import Docker
from buildtools.target import Target
from buildtools.target import TargetScanner
from buildtools.gitlab import GitLabYAMLGenerator


logger = logging.getLogger(__name__)


def conv_target_to_env(target:str) -> str:

    target = target.upper()
    trans_table = str.maketrans(dict.fromkeys(string.punctuation, "_"))
    target = target.translate(trans_table)
    return '='.join([target, 'YES'])


def handle_git_commands(args):

    git = Git(branch=args.set_branch_name)

    logger.info(f"Git version: {git.version}, Git branch name: {git.branch_name}, Git commit id: {git.commit_id}")
    
    if args.info:
        print(f"Git version: {git.version}")
        print(f"Git branch name: {git.branch_name}")
        print(f"Git commit id: {git.commit_id}")

    elif args.get_branch_name:
        print(git.branch_name)

    elif args.get_target_branch:
        print(git.get_target_branch())

    elif args.fetch_target_branch:
        git.fetch_target_branch()

    elif args.show_changed_files:
        target_branch = git.get_target_branch()
        logger.info(f"The list of changed files from {target_branch} to {git.commit_id}")
        for _file in sorted(git.changed_files(from_commit=target_branch)):
            print(f"{_file}")


def handle_target_commands(args):

    if args.show_targets:
        scanner = TargetScanner()
        for target_path in scanner.run():
            print(f"- {target_path}")
    
    elif args.target_info:
        target = Target(args.target_info)
        print(target.info)

    elif args.show_changed_targets:
        git = Git(args.branch_name)
        scanner = TargetScanner()

        target_branch = git.get_target_branch()
        logger.info(f"The list of changed targes from {target_branch} to {git.commit_id}")

        targets_from_changed_files = set([Path(f).parent for f in git.changed_files(from_commit=target_branch)])
        all_targets = set([t for t in scanner.run()])
        for changed_target in all_targets.intersection(targets_from_changed_files):
            print(changed_target)

    elif args.generate_pipeline:
        git = Git(args.branch_name)
        scanner = TargetScanner()

        target_branch = git.get_target_branch()
        logger.info(f"The list of changed targes from {target_branch} to {git.commit_id}")

        changed_paths = set([Path(f).parent for f in git.changed_files(from_commit=target_branch)])
        all_targets = set([t for t in scanner.run()])
        
        changed_targets = all_targets.intersection(changed_paths)
        if changed_targets:
            generator = GitLabYAMLGenerator(branch_name=git.branch_name)
            generator.run(changed_targets)
        else:
            logger.warning('No changed targets')


def handle_docker_commands(args):

    target_path = args.target_path
    dev_image = args.dev_image

    docker = Docker(path=target_path, dev_image=dev_image)

    if args.build:
        docker.build()

    elif args.remove:
        docker.remove()

    elif args.test:
        docker.test()

    elif args.publish:
        docker.publish()

def run_cli():

    parser = argparse.ArgumentParser('buildtools')

    parser.add_argument('-l', '--log-level',
                        default='INFO',
                        help='Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL')

    subparsers = parser.add_subparsers()

    # Git commands
    git_parser = subparsers.add_parser('git', help='Git commands')
    git_parser.add_argument('--info', action='store_true', 
            help='print out general information')
    git_parser.add_argument('--set-branch-name', type=str, 
            help='specify branch name from CI tool')
    git_parser.add_argument('--get-branch-name', action='store_true', 
            help='get current branch name')
    git_parser.add_argument('--get-target-branch', action='store_true', 
            help='get target branch name')
    git_parser.add_argument('--fetch-target-branch', action='store_true', 
            help='fetch target branch name')
    git_parser.add_argument('--show-changed-files', action='store_true', 
            help='show changed files')
    git_parser.set_defaults(handler=handle_git_commands)

    # Target commands
    target_parser = subparsers.add_parser('target', help='Target commands')
    target_parser.add_argument('--branch-name', type=str, 
                                help='specify branch name from CI tool')
    target_parser.add_argument('--show-targets', action='store_true', 
                                help='show targets')
    target_parser.add_argument('--show-changed-targets', action='store_true', 
                                help='show changed targets')
    target_parser.add_argument('--generate-pipeline', action='store_true', 
                                help='generate Gitlab CI pipeline for changed targets')
    target_parser.add_argument('--target-info',  help='show targets')
    target_parser.set_defaults(handler=handle_target_commands)

    # Docker commands
    docker_parser = subparsers.add_parser('docker', help='Docker commads')
    docker_parser.add_argument('--target-path', type=str, required=True,
                                help='The path to target')
    docker_parser.add_argument('--build', action='store_true', 
                                help='build docker image for target')
    docker_parser.add_argument('--remove', action='store_true', 
                                help='remove docker image for target')
    docker_parser.add_argument('--test', action='store_true', 
                                help='test docker image for target')
    docker_parser.add_argument('--publish', action='store_true', 
                                help='publish docker image for target')
    docker_parser.add_argument('--dev-image', action='store_true', 
                                help='create dev image for target')
    docker_parser.set_defaults(handler=handle_docker_commands)

    # Main
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level,
                            format="%(asctime)s.%(msecs)03d (%(name)s) [%(levelname)s] %(message)s",
                            datefmt='%Y-%m-%dT%H:%M:%S')

    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
