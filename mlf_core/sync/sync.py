#!/usr/bin/env python
"""
Synchronise a project TEMPLATE branch with the template.
"""
import fnmatch
import logging
import sys
from configparser import ConfigParser, NoSectionError
from distutils.dir_util import copy_tree
from subprocess import Popen, PIPE
from typing import Tuple
import git
import json
import os
import requests
import shutil
import tempfile
from pathlib import Path
from github import Github
from packaging import version
from rich import print

from mlf_core.config.config import ConfigCommand
from mlf_core.create.github_support import decrypt_pat, load_github_username, create_sync_secret
from mlf_core.common.load_yaml import load_yaml_file
from mlf_core.create.create import choose_domain
from mlf_core.common.version import load_project_template_version_and_handle, load_mlf_core_template_version
from mlf_core.custom_cli.questionary import mlf_core_questionary_or_dot_mlf_core

log = logging.getLogger(__name__)


class TemplateSync:
    """
    Hold syncing information and results.

    project_dir (str): The path to the mlf-core project root directory
    from_branch (str): Original branch
    project_dir (str): Path to target project directory
    from_branch (str): Original branch
    original_branch (str): Repo branch that was checked out before we started.
    made_changes (bool): Whether making the new template project introduced any changes
    gh_username (str): GitHub username
    patch_update (bool): Whether a patch update was found for the template or not
    minor_update (bool): Whether a minor update was found for the template or not
    major_update (bool): Whether a major update was found for the template or not
    repo_owner (str): Owner of the repo (either orga name or personal github username)
    """

    def __init__(self,
                 project_dir,
                 new_template_version,
                 from_branch=None,
                 gh_username=None,
                 token=None,
                 major_update=False,
                 minor_update=False,
                 patch_update=False):
        self.project_dir = os.path.abspath(project_dir)
        self.from_branch = from_branch
        self.original_branch = None
        self.made_changes = False
        self.gh_pr_returned_data = {}
        self.major_update = major_update
        self.minor_update = minor_update
        self.patch_update = patch_update
        self.gh_username = gh_username if gh_username else load_github_username()
        self.token = token if token else decrypt_pat()
        self.dot_mlf_core = {}
        self.repo_owner = self.gh_username
        self.new_template_version = new_template_version

    def sync(self):
        """
        Sync the mlf-core project
        """
        self.inspect_sync_dir()
        self.checkout_template_branch()
        self.delete_template_branch_files()
        self.make_template_project()
        self.commit_template_changes()

        # Push and make a pull request
        if self.made_changes:
            try:
                self.push_template_branch()
                self.make_pull_request()
            except Exception as e:
                self.reset_target_dir()
                print(f'[bold red]{e}')
                sys.exit(1)

        self.reset_target_dir()

        if not self.made_changes:
            print('[bold blue]No changes made to TEMPLATE - sync complete')

    def inspect_sync_dir(self):
        """
        Examines target directory to sync, verifies that it is a git repository and ensures that there are no uncommitted changes.
        """
        if not os.path.exists(os.path.join(str(self.project_dir), '.mlf_core.yml')):
            print(f'[bold red]{self.project_dir} does not appear to contain a .mlf_core.yml file. Did you delete it?')
            sys.exit(1)
        # store .mlf_core.yml content for later reuse in the dry create run
        self.dot_mlf_core = load_yaml_file(os.path.join(str(self.project_dir), '.mlf_core.yml'))
        log.debug(f'Loaded .mlf_core.yml file content. Content is: {self.dot_mlf_core}')
        # Check that the project_dir is a git repo
        try:
            self.repo = git.Repo(self.project_dir)
        except git.exc.InvalidGitRepositoryError:
            print(f'[bold red]{self.project_dir} does not appear to be a git repository.')
            sys.exit(1)

        # get current branch so we can switch back later
        self.original_branch = self.repo.active_branch.name
        print(f'[bold blue]Original Project repository branch is {self.original_branch}')

        # Check to see if there are uncommitted changes on current branch
        if self.repo.is_dirty(untracked_files=True):
            print('[bold red]Uncommitted changes found in Project directory!\nPlease commit these before running mlf-core sync')
            sys.exit(1)

    def checkout_template_branch(self):
        """
        Try to check out the origin/TEMPLATE in a new TEMPLATE branch.
        If this fails, try to check out an existing local TEMPLATE branch.
        """
        try:
            self.from_branch = self.repo.active_branch.name
        except git.exc.GitCommandError as e:
            print(f'[bold red]Could not find active repo branch:\n{e}')
        # Try to check out the `TEMPLATE` branch
        try:
            self.repo.git.checkout('origin/TEMPLATE', b='TEMPLATE')
        except git.exc.GitCommandError:
            # Try to check out an existing local branch called TEMPLATE
            try:
                self.repo.git.checkout('TEMPLATE')
            except git.exc.GitCommandError:
                print('[bold red]Could not check out branch "origin/TEMPLATE" or "TEMPLATE"')
                sys.exit(1)

    def delete_template_branch_files(self):
        """
        Delete all files in the TEMPLATE branch
        """
        # Delete everything
        print('[bold blue]Deleting all files in TEMPLATE branch')
        for the_file in os.listdir(self.project_dir):
            if the_file == '.git':
                log.debug('Found .git directory. Skipping deleting it.')
                continue
            file_path = os.path.join(self.project_dir, the_file)
            try:
                if os.path.isfile(file_path):
                    log.debug(f'Deleting file {file_path}')
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    log.debug(f'Deleting directory {file_path}')
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'[bold red]{e}')
                sys.exit(1)

    def make_template_project(self):
        """
        Delete all files and make a fresh template.
        """
        print('[bold blue]Creating a new template project.')
        # dry create run from mlf-core in tmp directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            old_cwd = str(Path.cwd())
            log.debug(f'Saving current working directory {old_cwd}.')
            os.chdir(tmpdirname)
            log.debug(f'Changed directory to {tmpdirname}.')
            log.debug(f'Calling choose_domain with {self.dot_mlf_core}.')
            choose_domain(path=Path.cwd(), domain=None, dot_mlf_core=self.dot_mlf_core)
            # copy into the cleaned TEMPLATE branch's project directory
            log.debug(f'Copying created template into {self.project_dir}.')
            copy_tree(os.path.join(tmpdirname, self.dot_mlf_core['project_slug']), str(self.project_dir))
            log.debug(f'Changing directory back to {old_cwd}.')
            os.chdir(old_cwd)

    def commit_template_changes(self):
        """
        If we have any changes with the new template files, make a git commit
        """
        # Check that we have something to commit
        if not self.repo.is_dirty(untracked_files=True):
            print('[bold blue]Template contains no changes - no new commit created')
            return False
        # Commit changes
        try:
            # git add only non-blacklisted files
            print('[bold blue]Staging template.')
            # add all files to stage
            self.repo.git.add(A=True)
            # get all changed/modified files during the sync (including blacklisted ones)
            changed_files = [item.a_path for item in self.repo.index.diff('HEAD')]
            globs = self.get_blacklisted_sync_globs()
            blacklisted_changed_files = set()
            for pattern in globs:
                # keep track of all staged files matching a glob from the mlf_core.cfg file
                # those files will be excluded from syncing but will still be available in every new created projects
                blacklisted_changed_files |= {file for file in fnmatch.filter(changed_files, pattern)}
            nl = '\n'
            log.debug(f'Blacklisted (unsynced) files are:{nl}{nl.join(file for file in blacklisted_changed_files)}' if blacklisted_changed_files else
                      'No blacklisted files for syncing found.')
            # each blacklisted file must be first unstaged and then get its changes discarded, so it will not be marked as modified by git
            for blacklisted_file in blacklisted_changed_files:
                log.debug(f'Unstaging {blacklisted_file}')
                Popen(['git', 'reset', blacklisted_file], stdout=PIPE, stderr=PIPE, universal_newlines=True)
                log.debug(f'Discarding changes in working directory of file {blacklisted_file}')
                Popen(['git', 'checkout', '--', blacklisted_file], stdout=PIPE, stderr=PIPE, universal_newlines=True)

            files_to_commit = [file for file in changed_files if file not in blacklisted_changed_files]
            log.debug(f'Files to commit are:{nl}{nl.join(file for file in files_to_commit)}' if files_to_commit else
                      'No files to commit found.')
            if files_to_commit:
                print('[bold blue]Committing changes of non blacklisted files.')
                Popen(['git', 'commit', '-m', 'mlf-core sync', *files_to_commit], stdout=PIPE, stderr=PIPE, universal_newlines=True)
                print('[bold blue]Stashing and saving TEMPLATE branch changes!')
                Popen(['git', 'stash'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
                self.made_changes = True
                print('[bold blue]Committed changes to TEMPLATE branch')

            # if a file was added to the template, but is blacklisted, it remains untracked; so it should be removed
            for untracked_file in self.repo.untracked_files:
                log.debug(f'Removing untracked file {untracked_file}')
                Path(untracked_file).unlink()
        except Exception as e:
            print(f'[bold red]Could not commit changes to TEMPLATE:\n{e}')
            sys.exit(1)
        return True

    def push_template_branch(self):
        """
        If there are any changes to the template, push the TEMPLATE branch to the default remote
        and push to the actual sync temporary branch, where a PR is actually created from to development branch.
        """
        print(f'[bold blue]Pushing TEMPLATE branch to remote: {os.path.basename(self.project_dir)}')
        try:
            log.debug('Getting origin as remote.')
            origin = self.repo.remote('origin')
            log.debug('Setting TEMPLATE branch as upstream tracking branch.')
            self.repo.head.ref.set_tracking_branch(origin.refs.TEMPLATE)
            log.debug('Pushing to upstream branch TEMPLATE.')
            self.repo.git.push(force=True)
            print(f'[bold blue]Checking out to new branch mlf_core_sync_v{self.new_template_version}')
            log.debug(f'git checkout -b mlf_core_sync_v{self.new_template_version}')
            self.repo.git.checkout('-b', f'mlf_core_sync_v{self.new_template_version}')
            log.debug(f'git push origin mlf_core_sync_v{self.new_template_version}')
            print(f'[bold blue]Pushing to remote branch mlf_core_sync_v{self.new_template_version}')
            self.repo.remotes.origin.push(refspec=f'mlf_core_sync_v{self.new_template_version}:mlf_core_sync_v{self.new_template_version}')
        except git.exc.GitCommandError as e:
            print(f'Could not push TEMPLATE or mlf_core_sync_v{self.new_template_version} branch:\n{e}')
            sys.exit(1)

    def make_pull_request(self):
        """
        Create a pull request to a base branch from a head branch (that is, a temporary branch only created for syncing the new template version)
        """
        log.debug('Preparing PR contents to submit a sync PR.')
        if self.dot_mlf_core['is_github_orga']:
            self.repo_owner = self.dot_mlf_core['github_orga']
        pr_title = f'Important mlf-core template update {self.new_template_version} released!'
        pr_body_text = (
            'A new release of the main template in mlf-core has just been released. '
            'This automated pull-request attempts to apply the relevant updates to this Project.\n\n'
            'Please make sure to merge this pull-request as soon as possible. '
            'Once complete, make a new minor release of your Project.\n\n'
            'For more information on the actual changes, read the latest mlf-core changelog.')
        log.debug(f'PR title is {pr_title} and PR body: {pr_body_text}')

        # Check, whether a mlf-core sync PR is already open
        self.check_pull_request_exists()
        # Submit the new pull request with the latest mlf-core sync changes
        self.submit_pull_request(pr_title, pr_body_text)

    def submit_pull_request(self, pr_title, pr_body_text):
        """
        Create a new pull-request on GitHub
        """
        pr_content = {
            'title': pr_title,
            'body': pr_body_text,
            'maintainer_can_modify': True,
            'head': f'mlf_core_sync_v{self.new_template_version}',
            'base': 'development',
        }
        r = requests.post(
            url=f'https://api.github.com/repos/{self.repo_owner}/{self.dot_mlf_core["project_slug"]}/pulls',
            data=json.dumps(pr_content),
            auth=requests.auth.HTTPBasicAuth(self.gh_username, self.token),
        )
        try:
            self.gh_pr_returned_data = json.loads(r.content)
            returned_data_prettyprint = json.dumps(self.gh_pr_returned_data, indent=4)
        except requests.RequestException:
            self.gh_pr_returned_data = r.content
            returned_data_prettyprint = r.content

        # PR worked
        if r.status_code == 201:
            print('[bold blue]Successfully created PR!')

        # Something went wrong
        else:
            print(f'GitHub API returned code {r.status_code}: \n{returned_data_prettyprint}')
            sys.exit(1)

    def check_pull_request_exists(self) -> bool:
        """
        Check, whether a mlf-core sync PR is already open. If so, close this one, as it is outdated.

        :return Whether a mlf-core sync PR is already open or not
        """
        g = Github(self.token)
        repo = g.get_repo(f'{self.repo_owner}/{self.dot_mlf_core["project_slug"]}')
        # query all open PRs
        log.debug('Querying open PRs to check if a sync PR already exists.')
        # iterate over the open PRs of the repo to check if a mlf-core sync PR is open
        for pull_request in repo.get_pulls(state='open'):
            log.debug('Already open sync PR has been found.')
            # if an older, outdated mlf-core sync PR is still open, close it first
            if 'Important mlf-core template update' in pull_request.title:
                print('[bold blue]Detected open, but outdated mlf-core sync PR. Closing it in favor of the newest sync PR!')
                pull_request.edit(state='closed')
                return True
        return False

    def check_sync_level(self) -> bool:
        """
        Check whether a pull request should be made according to the set level in the mlf_core.cfg file.
        Possible levels are:
            - patch: Always create a pull request (lower bound)
            - minor: Create a pull request if it's a minor or major change
            - major: Create a pull request only if it's a major change
        :return: Whether the changes level is equal to or smaller than the set sync level; whether a PR should be created or not
        """
        log.debug(f'Checking sync level constraints using parsed results from {self.project_dir}/mlf_core.cfg')
        try:
            parser = ConfigParser()
            parser.read(f'{self.project_dir}/mlf_core.cfg')
            level_item = list(parser.items('sync_level'))
            log.debug(f'Parsing level constraint returned: {level_item}.')
            # check for proper configuration if the sync_level section (only one item named mlf_core_sync_level with valid levels major or minor
            if len(level_item) != 1 or 'sync_level' not in level_item[0][0] or not any(level_item[0][1] == valid_lvl for valid_lvl in
                                                                                       ['major', 'minor', 'patch']):
                print('[bold red]Your mlf_core_sync_level section is missconfigured. Make sure that it only contains one item named mlf_core_sync_level '
                      'with only valid levels patch, minor or major!')
                sys.exit(1)
            # check in case of minor update that level is not set to major (major case must not be handled as level is a lower bound)
            if self.patch_update:
                log.debug('Checking whether constraints allow patch updates.')
                return level_item[0][1] != 'minor' and level_item[0][1] != 'major'
            elif self.minor_update:
                log.debug('Checking whether constraints allow minor updates.')
                return level_item[0][1] != 'major'
            else:
                log.debug('All updates are allowed because patch level is set.')
                return True
        # mlf_core.cfg file was not found or has no section sync_level
        except NoSectionError:
            print('[bold red]Could not read from mlf_core.cfg file. '
                  'Make sure your specified path contains a mlf_core.cfg file and has a sync_level section!')
            sys.exit(1)

    def get_blacklisted_sync_globs(self) -> list:
        """
        Get all blacklisted globs from the mlf_core.cfg file.
        :return: A list of all blacklisted globs for sync (file (types) that should not be included into the sync pull request)
        """
        try:
            parser = ConfigParser()
            parser.read(f'{self.project_dir}/mlf_core.cfg')
            globs = list(parser.items('sync_files_blacklisted'))
            nl = '\n'
            log.debug(f'Returning all blacklisted files globs parsed from {self.project_dir}/mlf_core.cfg.')
            log.debug(f'Blacklisted globs were {nl}{nl.join(glob[1] for glob in globs)}')
            return [glob[1] for glob in globs]

        # mlf_core.cfg file was not found or has no section called sync_files_blacklisted
        except NoSectionError:
            print('[bold red]Could not read from mlf_core.cfg file. Make sure your specified path contains a mlf_core.cfg file and has a '
                  'sync_files_blacklisted section!')
            sys.exit(1)

    def reset_target_dir(self):
        """
        Reset the target project directory. Check out the original branch.
        """
        print(f'[bold blue]Checking out original branch: {self.original_branch}')
        try:
            self.repo.git.checkout(self.original_branch)
        except git.exc.GitCommandError as e:
            print(f'[bold red]Could not reset to original branch {self.from_branch}:\n{e}')
            sys.exit(1)

    @staticmethod
    def update_sync_token(project_name: str, gh_username: str = '') -> None:
        """
        Update the sync token secret for the repository.

        :param project_name Name of the users project
        :param gh_username The Github username (only gets passed, if the repo is an orga repo)
        """
        gh_username = load_yaml_file(ConfigCommand.CONF_FILE_PATH)['github_username'] if not gh_username else gh_username
        # get the personal access token for user authentification
        log.debug('Asking for updated sync token value.')
        updated_sync_token = mlf_core_questionary_or_dot_mlf_core(function='password',
                                                                  question='Please enter your updated sync token value')
        print(f'[bold blue]\nUpdating sync secret for project {project_name}.')
        create_sync_secret(gh_username, project_name, updated_sync_token)
        print(f'[bold blue]\nSuccessfully updated sync secret for project {project_name}.')

    @staticmethod
    def has_template_version_changed(project_dir: Path) -> Tuple[bool, bool, bool, str, str]:
        """
        Check, if the mlf-core template has been updated since last check/sync of the user.

        :return: Both false if no versions changed or a micro change happened (for ex. 1.2.3 to 1.2.4). Return is_major_update True if a major version release
        happened for the mlf-core template (for example 1.2.3 to 2.0.0). Return is_minor_update True if a minor change happened (1.2.3 to 1.3.0).
        Return is_patch_update True if its a micro update (for example 1.2.3 to 1.2.4).
        mlf-core will use this to decide which syncing strategy to apply. Also return both versions.
        """
        # Try to compare against the development branch, since it is the most up to date (usually).
        # If a development branch does not exist compare against master.
        repo = git.Repo(project_dir)
        try:
            repo.git.checkout('development')
        except git.exc.GitCommandError:
            print('[bold red]Could not checkout development branch. Trying to checkout master...')
            try:
                repo.git.checkout('master')
            except git.exc.GitCommandError as e:
                print(f'[bold red]Could not checkout master branch.\n{e}')
                sys.exit(1)

        log.debug('Loading the project\'s template version and the mlf-core template version.')
        template_version_last_sync, template_handle = TemplateSync.sync_load_project_template_version_and_handle(project_dir)
        template_version_last_sync = version.parse(template_version_last_sync)  # type: ignore
        current_mlf_core_template_version = version.parse(TemplateSync.sync_load_template_version(template_handle))
        log.debug(f'Projects template version is {template_version_last_sync} and mlf-core template version is {current_mlf_core_template_version}')
        is_major_update, is_minor_update, is_patch_update = False, False, False

        # check if a major change happened (for example 1.2.3 to 2.0.0)
        if template_version_last_sync.major < current_mlf_core_template_version.major:  # type: ignore
            is_major_update = True
        # check if minor update happened (for example 1.2.3 to 1.3.0)
        elif template_version_last_sync.minor < current_mlf_core_template_version.minor:  # type: ignore
            is_minor_update = True
        # check if a patch update happened (for example 1.2.3 to 1.2.4)
        elif template_version_last_sync.micro < current_mlf_core_template_version.micro:  # type: ignore
            is_patch_update = True
        return is_major_update, is_minor_update, is_patch_update, str(template_version_last_sync), str(current_mlf_core_template_version)

    @staticmethod
    def sync_load_template_version(handle: str) -> str:
        """
        Load the version of the template available from mlf-core specified by the handler for syncing.

        :param handle: The template handle
        :return: The actual version number of the template in mlf-core
        """
        top_path = f'{os.path.dirname(__file__)}/..'
        available_templates_path = f'{str(top_path)}/create/templates/available_templates.yml'
        log.debug(f'Using available templates file from {available_templates_path} to load current mlf-core template version.')
        return load_mlf_core_template_version(handle, available_templates_path)

    @staticmethod
    def sync_load_project_template_version_and_handle(project_dir: Path) -> Tuple[str, str]:
        """
        Return the project template version since last sync for user (if no sync happened, return initial create version of the template)

        :param project_dir: Top level path to users project directory
        """
        return load_project_template_version_and_handle(project_dir)
