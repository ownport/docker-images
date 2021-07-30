#
import json
import string
import logging

from pathlib import Path
from argparse import ArgumentParser

from importlib.machinery import SourceFileLoader

from buildtools.git import Git
from buildtools.gitlab import GitLabYAMLGenerator


logger = logging.getLogger(__name__)


def conv_target_to_env(target:str) -> str:

    target = target.upper()
    trans_table = str.maketrans(dict.fromkeys(string.punctuation, "_"))
    target = target.translate(trans_table)
    return '='.join([target, 'YES'])


class TargetBase:

    def __init__(self, path:str=None) -> None:

        if not path:
            self._path = Path.cwd()        
        elif path and Path(path).exists():
            self._path = Path(path)
        else:
            raise RuntimeError(f'The path does not exist, {path}')

    @property
    def path(self) -> Path:
        return self._path


class Target(TargetBase):

    def __init__(self, path: str) -> None:
        super().__init__(path=path)
        self._target_path = self._path.joinpath('TARGET')
        logger.info(f'Target path: {self._target_path}')

        target_module = SourceFileLoader('TARGET', str(self._target_path.absolute())).load_module()
        self._metadata = target_module.TARGET

    @property
    def info(self):
        ''' returns target metadata
        '''
        return self._metadata


class TargetScanner(TargetBase):

    def run(self):
        ''' run scanning of targets in path
        '''
        for target_file in self._path.glob("**/TARGET"):
            target_path = target_file.relative_to(self._path).parent 
            yield target_path

        # print('\nDepreacted targets:')
        # for target_file in self._path.glob("**/metadata"):
        #     target_path = target_file.relative_to(self._path).parent 
        #     print(f"- {target_path}")


def add_target_argumens(parser: ArgumentParser) -> ArgumentParser:

    parser.add_argument('--branch', type=str, nargs='?', default=None,
                                help='specify branch from CI tool')
    parser.add_argument('--tag', type=str, nargs='?', default=None,
                                help='specify tag from CI tool')
    parser.add_argument('--show-targets', action='store_true', 
                                help='show targets')
    parser.add_argument('--show-changed-targets', action='store_true', 
                                help='show changed targets')
    parser.add_argument('--generate-pipeline', action='store_true', 
                                help='generate Gitlab CI pipeline for changed targets')
    parser.add_argument('--target-info',  help='show targets')
    parser.set_defaults(handler=handle_cli_commands)

    return parser


def handle_cli_commands(args):

    if args.show_targets:
        scanner = TargetScanner()
        for target_path in sorted(scanner.run()):
            print(f"- {target_path}")
    
    elif args.target_info:
        target = Target(args.target_info)
        print(json.dumps(target.info))

    elif args.show_changed_targets:
        git = Git(args.branch)
        scanner = TargetScanner()

        target_branch = git.get_target_branch()
        logger.info(f"The list of changed targets from {git.commit_id} [{git.branch_name}] to {target_branch}")

        targets_from_changed_files = set([Path(f).parent for f in git.changed_files(from_commit=target_branch)])
        all_targets = set([t for t in scanner.run()])
        for changed_target in all_targets.intersection(targets_from_changed_files):
            print(changed_target)

    elif args.generate_pipeline:
        
        git = Git(branch=args.branch, tag=args.tag)
        scanner = TargetScanner()

        target_branch = git.get_target_branch()
        logger.info(f"The list of changed targes from {git.commit_id} [{git.branch_name}] to {target_branch}")

        changed_paths = set([Path(f).parent for f in git.changed_files(from_commit=target_branch)])
        all_targets = set([t for t in scanner.run()])
        
        changed_targets = all_targets.intersection(changed_paths)

        generator = GitLabYAMLGenerator(branch=git.branch_name)
        generator.run(changed_targets)

        if not changed_targets:
            logger.warning('No changed targets')