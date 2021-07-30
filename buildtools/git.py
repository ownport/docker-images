# Modified version of https://github.com/pantsbuild/pants/blob/main/src/python/pants/vcs/git.py
#       Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
#       Licensed under the Apache License, Version 2.0 (see LICENSE).

import re
import json
import logging
import subprocess

from argparse import ArgumentParser

from buildtools.fs import pushd
from buildtools.command import Command


logger = logging.getLogger(__name__)

# Regexps for branch names
RE_FEATURE_BRANCH = re.compile(r"^(?:origin/)?(feature/.+)")
RE_BUGFIX_BRANCH = re.compile(r"^(?:origin/)?(bugfix/.+)")
RE_DEVEL_BRANCH = re.compile(r"^(?:origin/)?devel")
RE_MASTER_BRANCH = re.compile(r"^(?:origin/)?master")


class Git:

    def __init__(self, branch:str=None, tag:str=None) -> None:
        """Creates a git scm proxy that assumes the git repository is in the cwd by default.

        branch :   The branch name, it can be specified via CI
        """
        self._gitcmd = "git"
        self._branch = branch
        self._tag = tag
        logger.info(f'The branch name from CI: {branch}')

    @property
    def current_rev_identifier(self):
        return "HEAD"

    @property
    def commit_id(self):
        return self._check_output(["rev-parse", "HEAD"])

    @property
    def version(self):
        ''' returns git version
        '''
        return self._check_output(["version", ]).replace('git version', '').strip()

    @property
    def branch_name(self):
        ''' returns branch name
        '''
        if not self._branch:
            self._branch = self.git_branch_name
        return self._branch

    @property
    def tag(self):

        return self._tag

    @property
    def git_branch_name(self):
        ''' returns branch name from git
        '''
        return self._check_output(["rev-parse", "--abbrev-ref", "HEAD"])

    @property
    def status(self):
        ''' return current Git status
        '''
        return {
            'gitVersion': self.version,
            'gitBranchName': self.git_branch_name,
            'gitTargetBranch': self.get_target_branch(),
            'gitCommitId': self.commit_id,
            'ciBranchName': self.branch_name,
            'ciTagName': self.tag,
        }

    def changed_files(self, 
            from_commit=None, 
            include_untracked=False):
        
        uncommitted_changes = self._check_output(["diff", "--name-only", "HEAD"])

        files = set(uncommitted_changes.splitlines())
        if from_commit:
            # Grab the diff from the merge-base to HEAD using ... syntax.  This ensures we have just
            # the changes that have occurred on the current branch.
            committed_cmd = ["diff", "--name-only", from_commit + f"...{self.commit_id}"]
            committed_changes = self._check_output(committed_cmd)
            files.update(committed_changes.split())

        if include_untracked:
            untracked_cmd = [
                "ls-files",
                "--other",
                "--exclude-standard",
                "--full-name",
            ]
            untracked = self._check_output(untracked_cmd)
            files.update(untracked.split())
        return files

    def changes_in(self, diffspec, relative_to=None):

        relative_to = relative_to or self._worktree
        cmd = ["diff-tree", "--no-commit-id", "--name-only", "-r", diffspec]
        return self._check_output(cmd).split()

    def commit(self, message, verify=True):

        cmd = ["commit", "--all", "--message=" + message]
        if not verify:
            cmd.append("--no-verify")
        self._check_call(cmd)

    def get_target_branch(self) -> str:
        ''' returns target branch name based on the name of current branch

        for feature/bugfix branch -> origin/devel
        for devel branch -> origin/master
        for master branch -> ""
        '''
        result = ""
        if RE_FEATURE_BRANCH.match(self.branch_name) or RE_BUGFIX_BRANCH.match(self.branch_name):
            result = 'origin/devel'
        elif RE_DEVEL_BRANCH.match(self.branch_name) or RE_MASTER_BRANCH.match(self.branch_name):
            result = "origin/master"
        return result

    def fetch_target_branch(self):
        ''' fetch target branch
        '''
        cmd = ["fetch", ]
        if not RE_MASTER_BRANCH.match(self.git_branch_name) and not self.tag:
            target_branch_name = self.get_target_branch().split("/")
            cmd += target_branch_name
        self._check_call(cmd)

    def get_last_tags(self, tags:int=1) -> list:
        ''' return the list of last tags, sorted by descending tag date
        '''
        cmd = ["for-each-ref", "refs/tags", "--sort=-taggerdate", "--format='%(tag)'", f"--count={tags}"]
        return self._check_output(cmd).replace("'", "").split('\n')

    def add(self, *paths) -> None:

        self._check_call(["add"] + list(paths))

    def _check_call(self, args, failure_msg=None) -> None:

        cmd = self._create_git_cmdline(args)
        self._log_call(cmd)
        result = subprocess.call(cmd)
        Command.check_result(cmd, result, failure_msg)

    def _check_output(self, args, failure_msg=None, errors="strict"):

        cmd = self._create_git_cmdline(args)
        self._log_call(cmd)
        process, out = Command.invoke(cmd)
        Command.check_result(cmd, process.returncode, failure_msg)
        return Command.cleanse(out, errors=errors)

    def _create_git_cmdline(self, args):
        
        return [self._gitcmd, ] + args

    def _log_call(self, cmd):
        logger.debug("Executing: " + " ".join(cmd))


def add_git_arguments(parser: ArgumentParser):
    
    parser.add_argument('--info', action='store_true', 
            help='print out general information')
    parser.add_argument('--branch', type=str, nargs='?', default=None,
            help='set branch from CI tool')
    parser.add_argument('--tag', type=str, nargs='?', default=None, 
            help='set tag from CI tool')
    parser.add_argument('--get-target-branch', action='store_true', 
            help='get target branch name')
    parser.add_argument('--fetch-target-branch', action='store_true', 
            help='fetch target branch name')
    parser.add_argument('--get-last-tags', type=int, default=None,
            help='get the list of last tags')
    parser.add_argument('--show-changed-files', action='store_true', 
            help='show changed files')
    parser.set_defaults(handler=handle_cli_commands)

    return parser


def handle_cli_commands(args):

    git = Git(branch=args.branch, tag=args.tag)

    logger.info(git.status)
    
    if args.info:
        print(json.dumps(git.status))

    elif args.get_target_branch:
        print(git.get_target_branch())

    elif args.fetch_target_branch:
        git.fetch_target_branch()

    elif args.get_last_tags:
        for tag in git.get_last_tags(tags=args.get_last_tags):
            print(tag)

    elif args.show_changed_files:
        target_branch = git.get_target_branch()
        logger.info(f"The list of changed files from {target_branch} to {git.commit_id}")
        for _file in sorted(git.changed_files(from_commit=target_branch)):
            print(f"{_file}")
    
    else:
        logger.warning('No action required, use --help to get more details')
    