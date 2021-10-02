#
import json
import string
import logging

from pathlib import Path
from argparse import ArgumentParser

from importlib.machinery import SourceFileLoader

from builder.git import Git
from builder.gitlab import GitLabYAMLGenerator

from builder.libs.yaml import safe_load as yaml_load
from builder.libs.yaml import safe_dump as yaml_dump
# try:
#     from builder.libs.yaml import CLoader as YAMLLoader
#     from builder.libs.yaml import CDumper as YAMLDumper
# except ImportError:
#     from builder.libs.yaml import Loader as YAMLLoader
#     from builder.libs.yaml import Dumper as YAMLDumper


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
        self._target_path = self._path.joinpath('TARGET.yml')
        logger.info(f'Target path: {self._target_path}')

        with open(self._target_path, 'r') as target_file:
            self._metadata = yaml_load(target_file)

    @property
    def info(self):
        ''' returns target metadata
        '''
        return self._metadata


class TargetScanner(TargetBase):

    def run(self):
        ''' run scanning of targets in path
        '''
        for target_file in self._path.glob("**/TARGET.yml"):
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

        targets_from_changed_files = set([Path(f).parent for f in git.changed_files()])
        all_targets = set([t for t in scanner.run()])
        for changed_target in all_targets.intersection(targets_from_changed_files):
            print(changed_target)

    elif args.generate_pipeline:
        
        git = Git(branch=args.branch, tag=args.tag)
        scanner = TargetScanner()

        changed_paths = set([Path(f).parent for f in git.changed_files()])
        all_targets = set([t for t in scanner.run()])
        
        changed_targets = all_targets.intersection(changed_paths)

        generator = GitLabYAMLGenerator(branch=git.branch_name, tag=args.tag)
        generator.run(changed_targets)

        if not changed_targets:
            logger.warning('No changed targets')
