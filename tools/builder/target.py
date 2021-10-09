#
import json
import string
import logging

from pathlib import Path
from argparse import ArgumentParser

from collections import defaultdict

from itertools import chain

flatten = chain.from_iterable

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping


from builder.git import Git
from builder.gitlab import GitLabYAMLGenerator

from builder.settings import Settings
from builder.libs.yaml import safe_load as yaml_load


logger = logging.getLogger(__name__)


def conv_target_to_env(target:str) -> str:

    target = target.upper()
    trans_table = str.maketrans(dict.fromkeys(string.punctuation, "_"))
    target = target.translate(trans_table)
    return '='.join([target, 'YES'])

def print_json(o:object) -> None:
    ''' print object as json string
    '''
    print(json.dumps(o))


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
        # logger.info(f'Target path: {self._target_path}')

        with open(self._target_path, 'r') as target_file:
            self._metadata = yaml_load(target_file)

    @property
    def info(self):
        ''' returns target metadata
        '''
        return self._metadata

    @staticmethod
    def root_path(filepath:Path) -> Path:
        ''' return a roor path to target by file path
        '''        
        path = filepath.parent
        if str(path) == '.':
            return None

        if not path.joinpath('TARGET.yml').exists():
            path = Target.root_path(path)
        return path

class TargetScanner(TargetBase):

    def run(self):
        ''' run scanning of targets in path
        '''
        for target_file in self._path.glob("**/TARGET.yml"):
            target_path = target_file.relative_to(self._path).parent 
            yield target_path


class TargetDeps(Mapping):
    ''' Representation of Target dependencies as directed acyclic graph
    using a dict (Mapping) as the underlying datastructure.
    '''
    def __init__(self) -> None:

        scanner = TargetScanner()
        self._deps = { 
            str(target_path): Target(target_path).info.get('depends', [])
                for target_path in sorted(scanner.run()) 
        }

    def __getitem__(self, *args):
        return self._deps.get(*args)

    def __iter__(self):
        return self._deps.__iter__()

    def __len__(self):
        return len(self._deps)
    
    def reverse(self) -> dict:
        ''' return a reversed dependency structure
        where a key is target and a value is a list of child targets 
        '''
        targets = defaultdict(list)
        for target, deps in self._deps.items():
            if len(deps) == 0:
                continue
            for parent in deps:
                targets[parent].append(target)

        # remove duplicatest in target's children
        for target, children in targets.items():
            targets[target] = list(set(children))
        
        return targets

    def parents(self, target:str) -> list:
        ''' return a list of target's parents
        '''
        _parents = list()
        for parent in self._deps.get(target, []):
            _parents.append(parent)
            _parents.extend(self.parents(parent))
        return sorted(set(_parents))

    def children(self, target:str) -> list:
        ''' return a list of target's children
        '''
        children = list()
        _deps = self.reverse()
        for child in _deps.get(target, []):
            children.append(child)
            children.extend(self.children(child))
        return sorted(set(children))
        

def add_target_argumens(parser: ArgumentParser) -> ArgumentParser:
    ''' add target CLI argeuments
    '''
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

    parser.add_argument('--info',  help='show targets')
    parser.add_argument('--deps', action='store_true', 
                                help='Show target dependencies, child -> parent')
    parser.add_argument('--reversed-deps', action='store_true', 
                                help='Show target dependencies in reversed form, parent -> child')
    parser.add_argument('--parents', type=str, 
                                help='show target parent(-s)')
    parser.add_argument('--children', type=str, 
                                help='show target children')
    parser.set_defaults(handler=handle_cli_commands)

    return parser


def handle_cli_commands(args):
    ''' handle CLI commands
    '''
    settings = Settings(args.settings)

    if args.show_targets:
        scanner = TargetScanner()
        for target_path in sorted(scanner.run()):
            print(f"- {target_path}")
    
    elif args.info:

        target = Target(args.info)
        print(json.dumps(target.info))

    elif args.show_changed_targets:

        git = Git(args.branch)
        deps = TargetDeps()

        changed_targets = set([
            Target.root_path(Path(f))
                for f in git.changed_files()
        ])
        changed_targets = sorted(map(str, filter(None, changed_targets)))
        changed_targets = changed_targets + list(flatten([deps.children(target) for target in changed_targets]))

        print_json(sorted(set(changed_targets)))

    elif args.generate_pipeline:
        
        git = Git(branch=args.branch, tag=args.tag)
        deps = TargetDeps()

        changed_targets = set([
            Target.root_path(Path(f))
                for f in git.changed_files()
        ])
        changed_targets = sorted(map(str, filter(None, changed_targets)))
        changed_targets = list(set(changed_targets + \
                            list(flatten([deps.parents(target) for target in changed_targets])) + \
                            list(flatten([deps.children(target) for target in changed_targets]))))

        generator = GitLabYAMLGenerator(branch=git.branch_name, 
                                        tag=args.tag, 
                                        settings=settings.get('gitlab', {}))
        generator.run(changed_targets)

        if not changed_targets:
            logger.warning('No changed targets')

    elif args.parents:

        _target = args.parents
        print_json(TargetDeps().parents(_target))

    elif args.children:

        _target = args.children
        print_json(TargetDeps().children(_target))

    elif args.deps:

        print_json(TargetDeps().items())

    elif args.reversed_deps:

        scanner = TargetScanner()
        targets = { str(target_path): Target(target_path).info.get('depends', [])
                        for target_path in sorted(scanner.run()) }

        print_json(TargetDeps(targets).reverse())
