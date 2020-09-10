import os
import sys
import appdirs
from pathlib import Path
from cryptography.fernet import Fernet
from ruamel.yaml import YAML
from rich import print
from rich.box import HEAVY_HEAD
from rich.style import Style
from rich.table import Table
from rich.console import Console

from mlf_core.common.levensthein_dist import most_similar_command
from mlf_core.custom_cli.questionary import mlf_core_questionary_or_dot_mlf_core
from mlf_core.common.load_yaml import load_yaml_file


class ConfigCommand:
    """
    Class for the config command. Sets general configurations such as full name, email and Github username.
    """
    # path where the config file is stored for mlf_core
    CONF_FILE_PATH = f'{appdirs.user_config_dir(appname="mlf_core")}/mlf_core_cfg.yml'
    KEY_PAT_FILE = f'{appdirs.user_config_dir(appname="mlf_core")}/.ct_keys'

    @staticmethod
    def all_settings() -> None:
        """
        Set general settings and PAT.
        """
        ConfigCommand.check_ct_config_dir_exists()
        ConfigCommand.config_general_settings()
        ConfigCommand.config_pat()

    @staticmethod
    def config_general_settings() -> None:
        """
        Set full_name and email for reuse in any project created further on.
        """
        ConfigCommand.check_ct_config_dir_exists()
        full_name = mlf_core_questionary_or_dot_mlf_core(function='text',
                                                         question='Full name',
                                                         default='Homer Simpson')
        email = mlf_core_questionary_or_dot_mlf_core(function='text',
                                                     question='Personal or work email',
                                                     default='homer.simpson@example.com')
        github_username = mlf_core_questionary_or_dot_mlf_core(function='text',
                                                               question='Github username',
                                                               default='HomerGithub').lower()

        # if the configs exist, just update them
        if os.path.exists(ConfigCommand.CONF_FILE_PATH):
            path = Path(ConfigCommand.CONF_FILE_PATH)
            yaml = YAML()
            settings = yaml.load(path)

            # update the full_name and email
            settings['full_name'] = full_name
            settings['email'] = email
            settings['github_username'] = github_username
            yaml.dump(settings, Path(ConfigCommand.CONF_FILE_PATH))

        # the configs don´t exist -> create them
        else:
            settings = {'full_name': full_name, 'email': email, 'github_username': github_username}
            yaml = YAML()
            yaml.dump(settings, Path(ConfigCommand.CONF_FILE_PATH))

    @staticmethod
    def config_pat() -> None:
        """
        Set the personal access token (PAT) for automatic Github repo creation.
        """
        ConfigCommand.check_ct_config_dir_exists()
        try:
            path = Path(ConfigCommand.CONF_FILE_PATH)
            yaml = YAML()
            settings = yaml.load(path)
            if not all(attr in settings for attr in ['full_name', 'github_username', 'email']):
                print('[bold red]The mlf-core config file misses some required attributes!')
                print('[bold blue]Lets set them before setting your Github personal access token!')
                ConfigCommand.config_general_settings()

        except FileNotFoundError:
            print('[bold red]Cannot find a mlf-core config file. Is this your first time using mlf-core?')
            print('[bold blue]Lets create one before setting your Github personal access token!')
            ConfigCommand.config_general_settings()

        if mlf_core_questionary_or_dot_mlf_core(function='confirm',
                                                question='Do you want to configure your GitHub personal access token right now?\n'
                                                'You can still configure it later '
                                                'by calling    mlf-core config pat',
                                                default='Yes'):
            access_token = mlf_core_questionary_or_dot_mlf_core(function='password',
                                                                question='Please enter your Github Access token')
            access_token_b = access_token.encode('utf-8')

            # ask for confirmation since this action will delete the PAT irrevocably if the user has not saved it anywhere else
            if not mlf_core_questionary_or_dot_mlf_core(function='confirm',
                                                        question='You´re about to update your personal access token. This action cannot be undone!\n'
                                                                 'Do you really want to continue?',
                                                        default='Yes'):
                sys.exit(1)

            # encrypt the given PAT and save the encryption key and encrypted PAT in separate files
            print('[bold blue]Generating key for encryption.')
            key = Fernet.generate_key()
            fer = Fernet(key)
            print('[bold blue]Encrypting personal access token.')
            encrypted_pat = fer.encrypt(access_token_b)

            # write key
            with open(ConfigCommand.KEY_PAT_FILE, 'wb') as f:
                f.write(key)

            path = Path(ConfigCommand.CONF_FILE_PATH)
            yaml = YAML()
            settings = yaml.load(path)
            settings['pat'] = encrypted_pat
            yaml.dump(settings, Path(ConfigCommand.CONF_FILE_PATH))

    @staticmethod
    def view_current_config() -> None:
        """
        Print the current users cookietemple configuration.
        """
        # load current settings
        try:
            settings = load_yaml_file(ConfigCommand.CONF_FILE_PATH)
            # create the table and print
            table = Table(title="[bold]Your current configuration", title_style="blue", header_style=Style(color="blue", bold=True), box=HEAVY_HEAD)
            table.add_column('Name', style='green')
            table.add_column('Value', style='green')
            # add rows to the table consisting of the name and value of the current setting
            for (name, value) in settings.items():
                # don't print token directly, just inform it's set
                if name == 'pat':
                    table.add_row('[bold]Personal access token', 'TOKEN_IS_SET')
                else:
                    table.add_row(f'[bold]{name.capitalize().replace("_", " ")}', f'[white]{value}')
            # don't print PAT directly but inform if not set
            if 'pat' not in settings.keys():
                table.add_row('[bold]Personal access token', '[red]NO_TOKEN_SET')

            console = Console()
            console.print(table)

        except (FileNotFoundError, KeyError):
            print('[bold red]Did not found a mlf-core config file!\nIf this is your first time running mlf-core you can set them using mlf-core '
                  'config general')

    @staticmethod
    def similar_handle(section: str) -> None:
        """
        Try to use/suggest a similar handle if user misspelled it.

        :param section: The handle inputted by the user.
        """
        com_list, action = most_similar_command(section.lower(), {'general', 'pat', 'all'})
        # use best match
        if len(com_list) == 1 and action == 'use':
            print(f'[bold blue]Unknown handle {section}. Will use best match {com_list[0]}.\n')
            ConfigCommand.handle_switcher().get(com_list[0], lambda: 'Invalid handle!')()
        # suggest best match
        elif len(com_list) == 1 and action == 'suggest':
            print(f'[bold blue]Unknown handle {section}. Did you mean {com_list[0]}?')
            sys.exit(1)
            # multiple best matches
        elif len(com_list) > 1:
            nl = '\n'
            print(f'[bold red]Unknown handle \'{section}\'.\nMost similar handles are: [green]{nl}{nl.join(sorted(com_list))}')
        else:
            # unknown handle and no best match found
            print('[bold red]Unknown handle. [green]See mlf-core --help [red]for more information on valid handles')

    @staticmethod
    def check_ct_config_dir_exists() -> None:
        """
        Check if the config directory for mlf-core exists. If not, create it.
        """
        if not os.path.exists(Path(ConfigCommand.CONF_FILE_PATH).parent):
            os.mkdir(Path(ConfigCommand.CONF_FILE_PATH).parent)

    @staticmethod
    def handle_switcher() -> dict:
        """
        Just a helper to switch between handles.

        :return: The switcher with all handles.
        """
        switcher = {
            'all': ConfigCommand.all_settings,
            'general': ConfigCommand.config_general_settings,
            'pat': ConfigCommand.config_pat
        }
        return switcher
