# -*- coding: utf-8 -*-

"""Entry point for mlf-core."""
import logging
import os
import sys
import click
from pathlib import Path

import rich.logging
from rich import traceback
from rich import print

import mlf_core
from mlf_core.bump_version.bump_version import VersionBumper
from mlf_core.config.config import ConfigCommand
from mlf_core.create.create import choose_domain
from mlf_core.custom_cli.click import HelpErrorHandling, print_project_version, CustomHelpSubcommand, CustomArg
from mlf_core.info.info import TemplateInfo
from mlf_core.lint.lint import lint_project
from mlf_core.list.list import TemplateLister
from mlf_core.custom_cli.questionary import mlf_core_questionary_or_dot_mlf_core
from mlf_core.sync.sync import TemplateSync
from mlf_core.upgrade.upgrade import UpgradeCommand
from mlf_core.common.load_yaml import load_yaml_file

WD = os.path.dirname(__file__)
log = logging.getLogger()


def main():
    traceback.install(width=200, word_wrap=True)
    print(r"""[bold blue]
███    ███ ██      ███████      ██████  ██████  ██████  ███████ 
████  ████ ██      ██          ██      ██    ██ ██   ██ ██      
██ ████ ██ ██      █████ █████ ██      ██    ██ ██████  █████ 
██  ██  ██ ██      ██          ██      ██    ██ ██   ██ ██    
██      ██ ███████ ██           ██████  ██████  ██   ██ ███████ 
                                                               
        """)

    print('[bold blue]Run [green]mlf-core --help [blue]for an overview of all commands\n')

    # Is the latest mlf-core version installed? Upgrade if not!
    if not UpgradeCommand.check_mlf_core_latest():
        print('[bold blue]Run [green]mlf-core upgrade [blue]to get the latest version.')
    mlf_core_cli()


@click.group(cls=HelpErrorHandling)
@click.version_option(mlf_core.__version__, message=click.style(f'mlf-core Version: {mlf_core.__version__}', fg='blue'))
@click.option('-v', '--verbose', is_flag=True, default=False, help='Enable verbose output (print debug statements).')
@click.option("-l", "--log-file", help="Save a verbose log to a file.")
@click.pass_context
def mlf_core_cli(ctx, verbose, log_file):
    """
    Create state of the art projects from production ready templates.
    """
    # Set the base logger to output DEBUG
    log.setLevel(logging.DEBUG)

    # Set up logs to the console
    log.addHandler(
        rich.logging.RichHandler(
            level=logging.DEBUG if verbose else logging.INFO,
            console=rich.console.Console(file=sys.stderr),
            show_time=True,
            markup=True,
        )
    )

    # Set up logs to a file if we asked for one
    if log_file:
        log_fh = logging.FileHandler(log_file, encoding="utf-8")
        log_fh.setLevel(logging.DEBUG)
        log_fh.setFormatter(logging.Formatter("[%(asctime)s] %(name)-20s [%(levelname)-7s]  %(message)s"))
        log.addHandler(log_fh)


@mlf_core_cli.command(short_help='Create a new project using one of our templates.', cls=CustomHelpSubcommand)
@click.option('--domain', type=click.Choice(['cli', 'lib', 'gui', 'web', 'pub']),
              help='The projects domain with currently cli, lib, gui, web and pub supported.')
def create(domain: str) -> None:
    """
    Create a new project using one of our templates.

    Creates a new project based on one of mlf-core's templates.
    You will be prompted for the domain, subdomain (if applicable), language and possibly framework.
    Template specific prompts follow. If you do not yet have a mlf-core config file you may be asked to create one first.
    Next, you will be asked whether you want to use mlf-core's Github support create a repository, push your template and enable a few settings.
    After the project has been created it will be linted and you will be notified of any TODOs.
    """
    choose_domain(domain, None)


@mlf_core_cli.command(short_help='Lint your existing mlf-core project.', cls=CustomHelpSubcommand)
@click.argument('project_dir', type=click.Path(), default=Path(str(Path.cwd())), helpmsg='Relative path to projects directory.', cls=CustomArg)
def lint(project_dir) -> None:
    """
    Lint your existing mlf-core project.

    Verify that your existing project still adheres to mlf_core's standards.
    mlf-core runs several general linting functions, which all templates share.
    Examples include a consistent project version, the existence of documentation and whether cookiecutter statements are still left.
    Afterwards, template specific linting is invoked. cli-python for example may check for the existence of a setup.py file.
    Both results are collected and displayed.
    """
    lint_project(project_dir)


@mlf_core_cli.command(short_help='List all available mlf-core templates.', cls=CustomHelpSubcommand)
def list() -> None:
    """
    List all available mlf-core templates.

    Get an overview of all existing mlf-core templates.
    The output only consists of a short description for all templates.
    To get a detailed overview of a specific subset of templates use info.
    """
    TemplateLister.list_available_templates()


@mlf_core_cli.command(short_help='Get detailed info on a mlf-core template domain or a single template.', cls=CustomHelpSubcommand)
@click.argument('handle', type=str, required=False, helpmsg='Language/domain of templates of interest.', cls=CustomArg)
@click.pass_context
def info(ctx, handle: str) -> None:
    """
    Get detailed info on a mlf_core template domain or a single template.

    list only provides an overview of all templates.
    Info provides a long description for a specific subset of templates.
    Pass a domain, language or full handle (e.g. cli-python).
    """
    if not handle:
        HelpErrorHandling.args_not_provided(ctx, 'info')
    else:
        template_info = TemplateInfo()
        template_info.show_info(handle.lower())


@mlf_core_cli.command(short_help='Sync your project with the latest template release.', cls=CustomHelpSubcommand)
@click.argument('project_dir', type=str, default=Path(f'{Path.cwd()}'),
                helpmsg='The projects top level directory you would like to sync. Default is current ''working directory.', cls=CustomArg)
@click.option('--set-token', '-st', is_flag=True, help='Set sync token to a new personal access token of the current repo owner.')
@click.argument('pat', type=str, required=False, helpmsg='Personal access token. Not needed for manual, local syncing!', cls=CustomArg)
@click.argument('username', type=str, required=False, helpmsg='Github username. Not needed for manual, local syncing!', cls=CustomArg)
@click.option('--check-update', '-ch', is_flag=True, help='Check whether a new template version is available for your project.')
def sync(project_dir, set_token, pat, username, check_update) -> None:
    """
    Sync your project with the latest template release.
    mlf_core regularly updates its templates.
    To ensure that you have the latest changes you can invoke sync, which submits a pull request to your Github repository (if existing).
    If no repository exists the TEMPLATE branch will be updated and you can merge manually.
    """
    project_dir_path = Path(f'{Path.cwd()}/{project_dir}') if not str(project_dir).startswith(str(Path.cwd())) else Path(project_dir)
    project_data = load_yaml_file(f'{project_dir}/.mlf_core.yml')

    # if set_token flag is set, update the sync token value and exit
    if set_token:
        try:
            if project_data['is_github_repo']:
                TemplateSync.update_sync_token(project_name=project_data['project_slug'], gh_username=project_data['github_username'])
            else:
                print('[bold red]Your current project does not seem to have a Github repository!')
                sys.exit(1)
        except FileNotFoundError:
            print(f'[bold red]There exists no .mlf_core.yml file at {project_dir_path}. Is this a mlf-core project?')
        except KeyError:
            print('[bold red]Your token value is not a valid personal access token for your account.')
            sys.exit(1)
        sys.exit(0)

    syncer = TemplateSync(new_template_version='', project_dir=project_dir_path, gh_username=username, token=pat, repo_owner=project_data['github_username'])
    # check for template version updates
    major_change, minor_change, patch_change, project_template_version, mlf_core_template_version = syncer.has_template_version_changed(project_dir_path)
    syncer.new_template_version = mlf_core_template_version
    # check for user without actually syncing
    if check_update:
        # a template update has been released by mlf-core
        if any(change for change in (major_change, minor_change, patch_change)):
            print(f'[bold blue]Your templates version received an update from {project_template_version} to {mlf_core_template_version}!\n'
                  f' Use [green]mlf-core sync [blue]to sync your project')
        else:
            print('[bold blue]Using the latest template version. No sync required.')
        # exit without syncing
        sys.exit(0)

    # set sync flags indicating a major, minor or patch update
    syncer.major_update = major_change
    syncer.minor_update = minor_change
    syncer.patch_update = patch_change

    # sync the project if any changes were detected
    if any(change for change in (major_change, minor_change, patch_change)):
        # If required sync level is set -> sync
        if syncer.check_sync_level():
            syncer.sync()
        else:
            print('[bold red]Aborting sync due to set level constraints. '
                  'You can set the level any time in your mlf_core.cfg in the sync_level section and sync again.')
    else:
        print('[bold blue]No changes detected. Your template is up to date.')


@mlf_core_cli.command('bump-version', short_help='Bump the version of an existing mlf-core project.', cls=CustomHelpSubcommand)
@click.argument('new_version', type=str, required=False, helpmsg='New project version in a valid format.', cls=CustomArg)
@click.argument('project-dir', type=click.Path(), default=Path(f'{Path.cwd()}'), helpmsg='Relative path to the projects directory.', cls=CustomArg)
@click.option('--downgrade', '-d', is_flag=True, help='Set this flag to downgrade a version.')
@click.option('--project-version', is_flag=True, callback=print_project_version, expose_value=False, is_eager=True, help='Print your projects version and exit')
@click.pass_context
def bump_version(ctx, new_version, project_dir, downgrade) -> None:
    """
    Bump the version of an existing mlf-core project.

    INFO on valid versions: All versions must match the format like 1.0.0 or 1.1.0-SNAPSHOT; these are the only valid
    version formats mlf-core allows. A valid version therefore contains a three digits (in the range from 0 to however large it will grow)
    separated by two dots.
    Optional is the -SNAPSHOT at the end (for JVM templates especially). NOTE that versions like 1.2.3.4 or 1.2 WILL NOT be recognized as valid versions as
    well as no substring of them will be recognized.

    Unless the user uses downgrade mode via the -d flag, a downgrade of a version is never allowed. Note that bump-version with the new version
    equals the current version is never allowed, either with or without -d.
    """
    if not new_version:
        HelpErrorHandling.args_not_provided(ctx, 'bump-version')
    else:
        # if the path entered ends with a trailing slash remove it for consistent output
        if str(project_dir).endswith('/'):
            project_dir = Path(str(project_dir).replace(str(project_dir)[len(str(project_dir)) - 1:], ''))

        version_bumper = VersionBumper(project_dir, downgrade)
        # lint before run bump-version
        version_bumper.lint_before_bump()
        # only run bump-version if conditions are met
        if version_bumper.can_run_bump_version(new_version, project_dir):
            # only run "sanity" checker when the downgrade flag is not set
            if not downgrade:
                # if the check fails, ask the user for confirmation
                if version_bumper.check_bump_range(version_bumper.CURRENT_VERSION.split('-')[0], new_version.split('-')[0]):
                    version_bumper.bump_template_version(new_version, project_dir)
                elif mlf_core_questionary_or_dot_mlf_core(function='confirm',
                                                          question=f'Bumping from {version_bumper.CURRENT_VERSION} to {new_version} seems not reasonable.\n'
                                                          f'Do you really want to bump the project version?',
                                                          default='n'):
                    print('\n')
                    version_bumper.bump_template_version(new_version, project_dir)
            else:
                version_bumper.bump_template_version(new_version, project_dir)
        else:
            sys.exit(1)


@mlf_core_cli.command(short_help='Configure your general settings and github credentials.', cls=CustomHelpSubcommand)
@click.option('--view', '-v', is_flag=True, help='View the current mlf-core configuration.')
@click.argument('section', type=str, required=False, helpmsg='Section to configure (all, general or pat)', cls=CustomArg)
@click.pass_context
def config(ctx, view: bool, section: str) -> None:
    """
    Configure your general settings and Github credentials for reuse.
    Available options (sections) are:

    \b
    - general: set your fullname, email and Github username
    - pat: set your Github personal access token for Github repository creation
    - all: calls general and pat
    """
    if view:
        ConfigCommand.view_current_config()
        sys.exit(0)
    if section == 'general':
        # set the full_name and email for reuse in the creation process
        ConfigCommand.config_general_settings()
    elif section == 'pat':
        # set github username and encrypted personal access token
        ConfigCommand.config_pat()
    elif section == 'all':
        # set everything
        ConfigCommand.all_settings()
        # empty section argument causes a customized error
    elif not section:
        HelpErrorHandling.args_not_provided(ctx, 'config')
        # check if a similar section handle can be used/suggested
    else:
        ConfigCommand.similar_handle(section)


@mlf_core_cli.command(short_help='Fix artifact location path for local all mlruns.', cls=CustomHelpSubcommand)
@click.argument('path', type=str, default='.', required=False, helpmsg='Path to the root of the mlruns folder.', cls=CustomArg)
@click.pass_context
def fix_artifact_paths(ctx, path: str) -> None:
    """
    """
    for meta_yaml in Path(f'{path}/mlruns').rglob('meta.yaml'):
        if 'file' not in meta_yaml.absolute():
            print(f'[bold yellow] Skipping path fixing for: {meta_yaml.absolute()}. Run was not saved locally.')
        print(f'[bold blue] Fixing path for: {meta_yaml.absolute()}')
        with open(meta_yaml.absolute()) as meta_yaml_file:
            content = meta_yaml_file.readlines()
            if 'artifact_location' in content[0]:
                content[0] = f'artifact_location: file://{meta_yaml.absolute().__str__()[:-10]}\n'
            else:
                content[0] = f'artifact_uri: file://{meta_yaml.absolute().__str__()[:-10]}/artifacts\n'

        with open(meta_yaml.absolute(), 'w') as meta_yaml_file:
            meta_yaml_file.writelines(content)


@mlf_core_cli.command(short_help='Check for a newer version of mlf-core and upgrade if required.', cls=CustomHelpSubcommand)
def upgrade() -> None:
    """
    Checks whether the locally installed version of mlf-core is the latest.
    If not pip will be invoked to upgrade mlf-core to the latest version.
    """
    UpgradeCommand.check_upgrade_mlf_core()


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
