import os
from pathlib import Path
from dataclasses import dataclass

from mlf_core.create.github_support import prompt_github_repo
from mlf_core.create.template_creator import TemplateCreator
from mlf_core.create.domains.mlf_core_template_struct import MlfcoreTemplateStruct
from mlf_core.custom_cli.questionary import mlf_core_questionary_or_dot_mlf_core
from mlf_core.common.version import load_mlf_core_template_version


@dataclass
class TemplateStructPackage(MlfcoreTemplateStruct):
    """
    PACKAGE-PREDICTION
    """
    framework: str = ''  # which machine learning framework to use


class PackageCreator(TemplateCreator):

    def __init__(self):
        self.package_struct = TemplateStructPackage(domain='package')
        super().__init__(self.package_struct)
        self.WD_Path = Path(os.path.dirname(__file__))
        self.TEMPLATES_PACKAGE_PATH = f'{self.WD_Path.parent}/templates/package'

        '"" TEMPLATE VERSIONS ""'
        self.PACKAGE_PREDICTION_TEMPLATE_VERSION = load_mlf_core_template_version('package-prediction', self.AVAILABLE_TEMPLATES_PATH)

    def create_template(self, dot_mlf_core: dict or None):
        """
        Handles the package domain. Prompts the user for the language, general and domain specific options.
        """

        self.package_struct.language = mlf_core_questionary_or_dot_mlf_core(function='select',
                                                                            question='Choose the project\'s primary purpose',
                                                                            choices=['prediction'],
                                                                            default='prediction',
                                                                            dot_mlf_core=dot_mlf_core,
                                                                            to_get_property='language')

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration(dot_mlf_core)

        # switch case statement to prompt the user to fetch template specific configurations
        switcher = {
            'prediction': self.package_prediction_options,
        }
        switcher.get(self.package_struct.language)(dot_mlf_core)

        self.package_struct.is_github_repo, \
            self.package_struct.is_repo_private, \
            self.package_struct.is_github_orga, \
            self.package_struct.github_orga \
            = prompt_github_repo(dot_mlf_core)

        if self.package_struct.is_github_orga:
            self.package_struct.github_username = self.package_struct.github_orga
        # create the chosen and configured template
        super().create_template_without_subdomain(self.TEMPLATES_PACKAGE_PATH)

        # switch case statement to fetch the template version
        switcher_version = {
            'package': self.PACKAGE_PREDICTION_TEMPLATE_VERSION,
        }
        self.package_struct.template_version, self.package_struct.template_handle = switcher_version.get(
            self.package_struct.language), f'package-{self.package_struct.language.lower()}'

        # perform general operations like creating a GitHub repository and general linting
        super().process_common_operations(domain='package', language=self.package_struct.language, dot_mlf_core=dot_mlf_core)

    def package_prediction_options(self, dot_mlf_core: dict or None):
        """ Prompts for package-prediction specific options and saves them into the PackageTemplateStruct """
        self.package_struct.framework = mlf_core_questionary_or_dot_mlf_core(function='select',
                                                                             question='Choose a framework',
                                                                             choices=['pytorch', 'tensorflow', 'xgboost'],
                                                                             default='pytorch',
                                                                             dot_mlf_core=dot_mlf_core,
                                                                             to_get_property='framework')
