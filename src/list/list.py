import os
import logging
from rich.style import Style
from rich.console import Console
from rich.table import Table
from rich.box import HEAVY_HEAD
from rich import print

from mlf_core.util.dict_util import is_nested_dictionary
from mlf_core.common.load_yaml import load_yaml_file

log = logging.getLogger(__name__)


class TemplateLister:
    """
    A class responsible for listing all available mlf-core templates in a nice layout
    """
    WD = os.path.dirname(__file__)
    TEMPLATES_PATH = f'{WD}/../create/templates'

    @classmethod
    def list_available_templates(cls) -> None:
        """
        Displays all available templates to stdout in nicely formatted yaml format.
        Omits long descriptions.
        """
        log.debug(f'Reading available_templates.yml at {cls.TEMPLATES_PATH}/available_templates.yml')
        available_templates = load_yaml_file(f'{cls.TEMPLATES_PATH}/available_templates.yml')
        print('[bold blue]Run [green]mlf-core info [blue]for long descriptions of your template of interest')
        print()

        # What we want to have are lists like
        # [['name', 'handle', 'short description', 'available libraries', 'version'], ['name', 'handle', 'short description', 'available libraries', 'version']]
        log.debug('Building list table.')
        templates_to_tabulate = []
        for language in available_templates.values():
            for val in language.values():
                # has a subdomain -> traverse dictionary a level deeper
                if is_nested_dictionary(val):
                    for val_2 in val.values():
                        templates_to_tabulate.append([
                            val_2['name'], val_2['handle'], val_2['short description'], val_2['available libraries'], val_2['version']
                        ])
                else:
                    templates_to_tabulate.append([
                        val['name'], val['handle'], val['short description'], val['available libraries'], val['version']
                    ])

        table = Table(title="[bold]All available mlf-core templates", title_style="blue", header_style=Style(color="blue", bold=True), box=HEAVY_HEAD)

        table.add_column("Name", justify="left", style="green", no_wrap=True)
        table.add_column("Handle", justify="left")
        table.add_column("Short Description", justify="left")
        table.add_column("Available Libraries", justify="left")
        table.add_column("Version", justify="left")

        for template in templates_to_tabulate:
            table.add_row(f'[bold]{template[0]}', template[1], template[2], template[3], template[4])

        console = Console()
        log.debug('Printing list table.')
        console.print(table)
