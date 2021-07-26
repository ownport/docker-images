# Modified version of https://github.com/pantsbuild/pants/blob/main/src/python/pants/vcs/git.py
#       Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
#       Licensed under the Apache License, Version 2.0 (see LICENSE).

import os
import re
import logging
import subprocess

from buildtools.fs import pushd
from buildtools.command import Command
from buildtools.command import CommandException


logger = logging.getLogger(__name__)

# Regexps for branch names
RE_FEATURE_BRANCH = re.compile(r"^(?:origin/)?(feature/.+)")
RE_DEVEL_BRANCH = re.compile(r"^(?:origin/)?devel")
RE_MASTER_BRANCH = re.compile(r"^(?:origin/)?master")


class Git:

    def __init__(self, branch=None):
        """Creates a git scm proxy that assumes the git repository is in the cwd by default.

        branch :   The branch name, it can be specified via CI
        """
        self._gitcmd = "git"
        self._branch = branch

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
            self._branch = self._check_output(["rev-parse", "--abbrev-ref", "HEAD"])
        return self._branch

    def changed_files(self, 
            from_commit=None, 
            include_untracked=False,
            relative_to=None):
        
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

        for feature branch -> origin/devel
        for devel branch -> origin/master
        '''
        result = ""
        if RE_FEATURE_BRANCH.match(self.branch_name):
            result = 'origin/devel'
        elif RE_DEVEL_BRANCH.match(self.branch_name):
            result = "origin/master"
        return result

    def fetch_target_branch(self):
        ''' fetch target branch
        '''
        target_branch_name = self.get_target_branch().split("/")
        cmd = ["fetch", ] + target_branch_name
        self._check_call(cmd)

    def add(self, *paths):

        self._check_call(["add"] + list(paths))

    def _check_call(self, args, failure_msg=None):

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


    