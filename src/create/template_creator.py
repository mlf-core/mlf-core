import os
import sys
import logging
from collections import OrderedDict
import shutil
import re
import tempfile
import requests
from distutils.dir_util import copy_tree
from pathlib import Path
from dataclasses import asdict
from ruamel.yaml import YAML
from cookiecutter.main import cookiecutter

import mlf_core
from mlf_core.custom_cli.questionary import mlf_core_questionary_or_dot_mlf_core
from mlf_core.util.dir_util import delete_dir_tree
from mlf_core.create.github_support import create_push_github_repository, load_github_username, is_git_repo
from mlf_core.lint.lint import lint_project
from mlf_core.util.docs_util import fix_short_title_underline
from mlf_core.create.domains.mlf_core_template_struct import MlfcoreTemplateStruct
from mlf_core.config.config import ConfigCommand
from mlf_core.common.load_yaml import load_yaml_file
from rich import print

log = logging.getLogger(__name__)


class TemplateCreator:
    """
    The base class for all creators.
    It holds the basic template information that are common across all templates (like a project name).
    Furthermore it defines methods that are basic for the template creation process.
    """

    def __init__(self, creator_ctx: MlfcoreTemplateStruct):
        self.WD = os.path.dirname(__file__)
        self.TEMPLATES_PATH = f'{self.WD}/templates'
        self.COMMON_FILES_PATH = f'{self.TEMPLATES_PATH}/common_all_files'
        self.COMMON_MLFLOW_FILES_PATH = f'{self.TEMPLATES_PATH}/common_mlflow_files'
        self.AVAILABLE_TEMPLATES_PATH = f'{self.TEMPLATES_PATH}/available_templates.yml'
        self.AVAILABLE_TEMPLATES = load_yaml_file(self.AVAILABLE_TEMPLATES_PATH)
        self.CWD = Path.cwd()
        self.creator_ctx = creator_ctx

    def process_common_operations(self, path: Path, skip_fix_underline=False,
                                  domain: str = None, subdomain: str = None, language: str = None,
                                  dot_mlf_core: OrderedDict = None) -> None:
        """
        Create all stuff that is common for mlf-core's template creation process; in detail those things are:
        create and copy common files, fix docs style, lint the project and ask whether the user wants to create a github repo.
        """
        # create the common files and copy them into the templates directory
        self.create_common_files(domain='all', common_files_path=self.COMMON_FILES_PATH)
        # key in the switcher indicates, whether there are domain specific files or not (None)
        domain_switcher = {
            'mlflow': 'mlflow',
            'package': None
        }
        # if project is a project with domain specific files, copy all common files for the domain of this project
        try:
            domain_specific_files = domain_switcher[self.creator_ctx.domain]
        # this should only be the case, if mlf-core is developed further and new domains are added, therefore the error message
        except KeyError:
            print(f'[bold red]Unknown domain {self.creator_ctx.domain}! This domain seems to be new and must be added into the domain switcher!')
            sys.exit(1)
        if domain_specific_files:
            self.create_common_files(domain=domain_specific_files, common_files_path=self.COMMON_MLFLOW_FILES_PATH)

        self.create_dot_mlf_core(template_version=self.creator_ctx.template_version)

        project_path = f'{self.CWD}/{self.creator_ctx.project_slug}'

        # Ensure that docs are looking good (skip if flag is set)
        if not skip_fix_underline:
            fix_short_title_underline(f'{project_path}/docs/index.rst')

        # Lint the project to verify that the new template adheres to all standards
        lint_project(project_path)

        if self.creator_ctx.is_github_repo and not dot_mlf_core:
            # rename the currently created template to a temporary name, create Github repo, push, remove temporary template
            tmp_project_path = f'{project_path}_mlf_core_tmp'
            os.mkdir(tmp_project_path)
            create_push_github_repository(project_path, self.creator_ctx, tmp_project_path)
            shutil.rmtree(tmp_project_path, ignore_errors=True)

        if subdomain:
            print(f'\n[bold blue]Please visit: https://mlf-core.readthedocs.io/en/latest/available_templates/available_templates.html'
                  f'#{domain}-{subdomain}-{language} for more information about how to use your chosen template.')
        else:
            print(f'\n[bold blue]Please visit: https://mlf-core.readthedocs.io/en/latest/available_templates/available_templates.html'
                  f'#{domain}-{language} for more information about how to use your chosen template.')

        # do not move if path is current working directory or a directory named like the project in the current working directory (second is default case)
        if path != self.CWD and path != Path(self.CWD / self.creator_ctx.project_slug_no_hyphen):
            shutil.move(f'{self.CWD}/{self.creator_ctx.project_slug_no_hyphen}', f'{path}/{self.creator_ctx.project_slug_no_hyphen}')

    def create_template_without_subdomain(self, domain_path: str) -> None:
        """
        Creates a chosen template that does **not** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        """
        # Target directory is already occupied -> overwrite?
        occupied = os.path.isdir(f'{self.CWD}/{self.creator_ctx.project_slug}')
        if occupied:
            self.directory_exists_warning()

            # Confirm proceeding with overwriting existing directory
            if mlf_core_questionary_or_dot_mlf_core('confirm', 'Do you really want to continue?', default='Yes'):
                cookiecutter(f'{domain_path}/{self.creator_ctx.domain}_{self.creator_ctx.language.lower()}',
                             no_input=True,
                             overwrite_if_exists=True,
                             extra_context=self.creator_ctx_to_dict())
            else:
                print('[bold red]Aborted! Canceled template creation!')
                sys.exit(0)
        else:
            cookiecutter(f'{domain_path}/{self.creator_ctx.domain}_{self.creator_ctx.language.lower()}',
                         no_input=True,
                         overwrite_if_exists=True,
                         extra_context=self.creator_ctx_to_dict())

    def create_template_with_subdomain(self, domain_path: str, subdomain: str) -> None:
        """
        Creates a chosen template that **does** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        :param subdomain: Subdomain of the chosen template
        """
        occupied = os.path.isdir(f'{self.CWD}/{self.creator_ctx.project_slug}')
        if occupied:
            self.directory_exists_warning()

            # Confirm proceeding with overwriting existing directory
            if mlf_core_questionary_or_dot_mlf_core('confirm', 'Do you really want to continue?', default='Yes'):
                delete_dir_tree(Path(f'{self.CWD}/{self.creator_ctx.project_slug}'))
                cookiecutter(f'{domain_path}/{subdomain}_{self.creator_ctx.language.lower()}',
                             no_input=True,
                             overwrite_if_exists=True,
                             extra_context=self.creator_ctx_to_dict())

            else:
                print('[bold red]Aborted! Canceled template creation!')
                sys.exit(0)
        else:
            cookiecutter(f'{domain_path}/{subdomain}_{self.creator_ctx.language.lower()}',
                         no_input=True,
                         overwrite_if_exists=True,
                         extra_context=self.creator_ctx_to_dict())

    def create_template_with_subdomain_framework(self, domain_path: str, subdomain: str, framework: str) -> None:
        """
        Creates a chosen template that **does** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        :param subdomain: Subdomain of the chosen template
        :param framework: Chosen framework
        """
        occupied = os.path.isdir(f'{self.CWD}/{self.creator_ctx.project_slug}')
        if occupied:
            self.directory_exists_warning()

            # Confirm proceeding with overwriting existing directory
            if mlf_core_questionary_or_dot_mlf_core('confirm', 'Do you really want to continue?', default='Yes'):
                cookiecutter(f'{domain_path}/{subdomain}_{self.creator_ctx.language.lower()}/{framework}',
                             no_input=True,
                             overwrite_if_exists=True,
                             extra_context=self.creator_ctx_to_dict())

            else:
                print('[bold red]Aborted! Canceled template creation!')
                sys.exit(0)
        else:
            cookiecutter(f'{domain_path}/{subdomain}_{self.creator_ctx.language.lower()}/{framework}',
                         no_input=True,
                         overwrite_if_exists=True,
                         extra_context=self.creator_ctx_to_dict())

    def prompt_general_template_configuration(self, dot_mlf_core: OrderedDict):
        """
        Prompts the user for general options that are required by all templates.
        Options are saved in the creator context manager object.
        """
        try:
            if dot_mlf_core:
                # try to read name and email from existing config file
                self.creator_ctx.full_name = dot_mlf_core['full_name']
                self.creator_ctx.email = dot_mlf_core['email']
            else:
                self.creator_ctx.full_name = load_yaml_file(ConfigCommand.CONF_FILE_PATH)['full_name']
                self.creator_ctx.email = load_yaml_file(ConfigCommand.CONF_FILE_PATH)['email']
        except FileNotFoundError:
            # style and automatic use config
            print('[bold red]Cannot find a mlf_core config file. Is this your first time using mlf-core?')
            # inform the user and config all settings (with PAT optional)
            print('[bold blue]Lets set your name, email and Github username and you´re ready to go!')
            ConfigCommand.all_settings()
            # load mail and full name
            path = Path(ConfigCommand.CONF_FILE_PATH)
            yaml = YAML(typ='safe')
            settings = yaml.load(path)
            # set full name and mail
            if dot_mlf_core:
                self.creator_ctx.full_name = dot_mlf_core['full_name']
                self.creator_ctx.email = dot_mlf_core['email']
            else:
                self.creator_ctx.full_name = settings['full_name']
                self.creator_ctx.email = settings['email']

        self.creator_ctx.project_name = mlf_core_questionary_or_dot_mlf_core(function='text',
                                                                             question='Project name',
                                                                             default='Exploding Springfield',
                                                                             dot_mlf_core=dot_mlf_core,
                                                                             to_get_property='project_name').lower()

        # check if the project name is already taken on readthedocs.io
        # lower the string, since mlflow doesn't play with uppercase docker container names
        while self.readthedocs_slug_already_exists(self.creator_ctx.project_name) and not dot_mlf_core:
            print(f'[bold red]A project named {self.creator_ctx.project_name} already exists at readthedocs.io!')
            if mlf_core_questionary_or_dot_mlf_core(function='confirm',
                                                    question='Do you want to choose another name for your project?\n'
                                                             'Otherwise you will not be able to host your docs at readthedocs.io!', default='Yes'):
                self.creator_ctx.project_name = mlf_core_questionary_or_dot_mlf_core(function='text',
                                                                                     question='Project name',
                                                                                     default='Exploding Springfield').lower()
            # break if the project should be named anyways
            else:
                break
        self.creator_ctx.project_slug = self.creator_ctx.project_name.replace(' ', '_')
        self.creator_ctx.project_slug_no_hyphen = self.creator_ctx.project_slug.replace('-', '_')
        self.creator_ctx.project_short_description = mlf_core_questionary_or_dot_mlf_core(function='text',
                                                                                          question='Short description of your project',
                                                                                          default=f'{self.creator_ctx.project_name}'
                                                                                                  f'. A mlf-core based .',
                                                                                          dot_mlf_core=dot_mlf_core,
                                                                                          to_get_property='project_short_description')
        poss_vers = mlf_core_questionary_or_dot_mlf_core(function='text',
                                                         question='Initial version of your project',
                                                         default='0.1.0-SNAPSHOT',
                                                         dot_mlf_core=dot_mlf_core,
                                                         to_get_property='version')

        # make sure that the version has the right format
        while not re.match(r'(?<!.)\d+(?:\.\d+){2}(?:-SNAPSHOT)?(?!.)', poss_vers) and not dot_mlf_core:
            print('[bold red]The version number entered does not match semantic versioning.\n' +
                  'Please enter the version in the format \[number].\[number].\[number](-SNAPSHOT)!')  # noqa: W605
            poss_vers = mlf_core_questionary_or_dot_mlf_core(function='text',
                                                             question='Initial version of your project',
                                                             default='0.1.0-SNAPSHOT')
        self.creator_ctx.version = poss_vers

        self.creator_ctx.license = mlf_core_questionary_or_dot_mlf_core(function='select',
                                                                        question='License',
                                                                        choices=['MIT', 'BSD', 'ISC', 'Apache2.0', 'GNUv3', 'Boost', 'Affero',
                                                                                 'CC0', 'CCBY', 'CCBYSA', 'Eclipse', 'WTFPL', 'unlicence',
                                                                                 'Not open source'],
                                                                        default='MIT',
                                                                        dot_mlf_core=dot_mlf_core,
                                                                        to_get_property='license')

        if dot_mlf_core:
            self.creator_ctx.github_username = dot_mlf_core['github_username']
            self.creator_ctx.creator_github_username = dot_mlf_core['creator_github_username']
        else:
            self.creator_ctx.github_username = load_github_username()
            self.creator_ctx.creator_github_username = self.creator_ctx.github_username

    def create_common_files(self, domain: str, common_files_path: str) -> None:
        """
        Create a temporary directory for common files of a specified domain or all templates and apply cookiecutter on them.
        They are subsequently moved into the directory of the created template.
        """
        log.debug('Creating common files.')
        dirpath = tempfile.mkdtemp()
        copy_tree(common_files_path, dirpath)
        cwd_project = self.CWD
        os.chdir(dirpath)
        log.debug(f'Cookiecuttering common files at {dirpath}')
        cookiecutter(dirpath,
                     extra_context={'full_name': self.creator_ctx.full_name,
                                    'email': self.creator_ctx.email,
                                    'language': self.creator_ctx.language,
                                    'domain': self.creator_ctx.domain,
                                    'project_name': self.creator_ctx.project_name,
                                    'project_slug': self.creator_ctx.project_slug,
                                    'project_slug_no_hyphen': self.creator_ctx.project_slug_no_hyphen,
                                    'version': self.creator_ctx.version,
                                    'license': self.creator_ctx.license,
                                    'project_short_description': self.creator_ctx.project_short_description,
                                    'github_username': self.creator_ctx.github_username,
                                    'creator_github_username': self.creator_ctx.creator_github_username,
                                    'framework': self.creator_ctx.language.capitalize() if domain == 'mlflow' else ''},
                     no_input=True,
                     overwrite_if_exists=True)

        # copy the common files directory content to the created project
        log.debug('Copying common files into the created project')
        copy_tree(f'{Path.cwd()}/common_{domain}_files', f'{cwd_project}/{self.creator_ctx.project_slug}')
        # delete the tmp cookiecuttered common files directory
        log.debug('Delete common files directory.')
        delete_dir_tree(Path(f'{Path.cwd()}/common_{domain}_files'))
        shutil.rmtree(dirpath)
        # change to recent cwd so lint can run properly
        os.chdir(str(cwd_project))

    def readthedocs_slug_already_exists(self, project_name: str) -> bool:
        """
        Test whether there´s already a project with the same name on readthedocs
        :param project_name Name of the project the user wants to create
        """
        print(f'[bold blue]Looking up {project_name} at readthedocs.io!')
        try:
            request = requests.get(f'https://{project_name.replace(" ", "")}.readthedocs.io')
            if request.status_code == 200:
                return True
        # catch exceptions when server may be unavailable or the request timed out
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print('[bold red]Cannot check whether name already taken on readthedocs.io because its unreachable at the moment!')
            return False

    def directory_exists_warning(self) -> None:
        """
        If the directory is already a git directory within the same project, print error message and exit.
        Otherwise print a warning that a directory already exists and any further action on the directory will overwrite its contents.
        """
        if is_git_repo(Path(f'{self.CWD}/{self.creator_ctx.project_slug}')):
            print(f'[bold red]Error: A git project named {self.creator_ctx.project_slug} already exists at [green]{self.CWD}\n')
            print('[bold red]Aborting!')
            sys.exit(1)
        else:
            print(f'[bold yellow]WARNING: [red]A directory named {self.creator_ctx.project_slug} already exists at [blue]{self.CWD}\n')
            print('Proceeding now will overwrite this directory and its content!')

    def create_dot_mlf_core(self, template_version: str):
        """
        Overrides the version with the version of the template.
        Dumps the configuration for the template generation into a .mlf_core yaml file.

        :param template_version: Version of the specific template
        """
        log.debug('Creating .mlf_core.yml file.')
        self.creator_ctx.template_version = f'{template_version} # <<MLF-CORE_NO_BUMP>>'
        self.creator_ctx.mlf_core_version = f'{mlf_core.__version__} # <<MLF-CORE_NO_BUMP>>'
        with open(f'{self.creator_ctx.project_slug}/.mlf_core.yml', 'w') as f:
            yaml = YAML()
            struct_to_dict = self.creator_ctx_to_dict()
            yaml.dump(struct_to_dict, f)

    def creator_ctx_to_dict(self) -> dict:
        """
        Create a dict from the our Template Structure dataclass
        :return: The dict containing all key-value pairs with non empty values
        """
        return {key: val for key, val in asdict(self.creator_ctx).items() if val != ''}
