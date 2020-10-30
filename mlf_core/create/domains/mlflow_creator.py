import os
from pathlib import Path
from dataclasses import dataclass

from mlf_core.create.github_support import prompt_github_repo
from mlf_core.create.template_creator import TemplateCreator
from mlf_core.create.domains.mlf_core_template_struct import MlfcoreTemplateStruct
from mlf_core.custom_cli.questionary import mlf_core_questionary_or_dot_mlf_core
from mlf_core.common.version import load_mlf_core_template_version


@dataclass
class TemplateStructMLflow(MlfcoreTemplateStruct):
    """
    MLFLOW-PYTORCH
    """
    command_line_interface: str = ''  # which command line library to use (click, argparse)
    testing_library: str = ''  # which testing library to use (pytest, unittest)


class MlflowCreator(TemplateCreator):

    def __init__(self):
        self.cli_struct = TemplateStructMLflow(domain='mlflow')
        super().__init__(self.cli_struct)
        self.WD_Path = Path(os.path.dirname(__file__))
        self.TEMPLATES_MLFLOW_PATH = f'{self.WD_Path.parent}/templates/mlflow'

        '"" TEMPLATE VERSIONS ""'
        self.MLFLOW_PYTORCH_TEMPLATE_VERSION = load_mlf_core_template_version('mlflow-pytorch', self.AVAILABLE_TEMPLATES_PATH)
        self.MLFLOW_TENSORFLOW_TEMPLATE_VERSION = load_mlf_core_template_version('mlflow-tensorflow', self.AVAILABLE_TEMPLATES_PATH)
        self.MLFLOW_XGBOOST_TEMPLATE_VERSION = load_mlf_core_template_version('mlflow-xgboost', self.AVAILABLE_TEMPLATES_PATH)
        self.MLFLOW_XGBOOST_DASK_TEMPLATE_VERSION = load_mlf_core_template_version('mlflow-xgboost_dask', self.AVAILABLE_TEMPLATES_PATH)

    def create_template(self, dot_mlf_core: dict or None):
        """
        Handles the mlflow domain. Prompts the user for the language, general and domain specific options.
        """

        self.cli_struct.language = mlf_core_questionary_or_dot_mlf_core(function='select',
                                                                        question='Choose the project\'s primary framework',
                                                                        choices=['pytorch', 'tensorflow', 'xgboost', 'xgboost_dask'],
                                                                        default='pytorch',
                                                                        dot_mlf_core=dot_mlf_core,
                                                                        to_get_property='language')

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration(dot_mlf_core)

        # switch case statement to prompt the user to fetch template specific configurations
        switcher = {
            'pytorch': self.mlflow_pytorch_options,
            'tensorflow': self.mlflow_tensorflow_options,
            'xgboost': self.mlflow_xgboost_options,
            'xgboost_dask': self.mlflow_xgboost_dask_options,
        }
        switcher.get(self.cli_struct.language)(dot_mlf_core)

        self.cli_struct.is_github_repo, \
            self.cli_struct.is_repo_private, \
            self.cli_struct.is_github_orga, \
            self.cli_struct.github_orga \
            = prompt_github_repo(dot_mlf_core)

        if self.cli_struct.is_github_orga:
            self.cli_struct.github_username = self.cli_struct.github_orga
        # create the chosen and configured template
        super().create_template_without_subdomain(self.TEMPLATES_MLFLOW_PATH)

        # switch case statement to fetch the template version
        switcher_version = {
            'pytorch': self.MLFLOW_PYTORCH_TEMPLATE_VERSION,
            'tensorflow': self.MLFLOW_TENSORFLOW_TEMPLATE_VERSION,
            'xgboost': self.MLFLOW_XGBOOST_TEMPLATE_VERSION,
            'xgboost_dask': self.MLFLOW_XGBOOST_DASK_TEMPLATE_VERSION
        }
        self.cli_struct.template_version, self.cli_struct.template_handle = switcher_version.get(
            self.cli_struct.language), f'mlflow-{self.cli_struct.language.lower()}'

        # perform general operations like creating a GitHub repository and general linting
        super().process_common_operations(domain='mlflow', language=self.cli_struct.language, dot_mlf_core=dot_mlf_core)

    def mlflow_pytorch_options(self, dot_mlf_core: dict or None):
        """ Prompts for mlflow-pytorch specific options and saves them into the MlflowTemplateStruct """
        pass

    def mlflow_tensorflow_options(self, dot_mlf_core: dict or None):
        """ Prompts for mlflow-tensorflow specific options and saves them into the MlflowTemplateStruct """
        pass

    def mlflow_xgboost_options(self, dot_mlf_core: dict or None):
        """ Prompts for mlflow-xgboost specific options and saves them into the MlflowTemplateStruct """
        pass

    def mlflow_xgboost_dask_options(self, dot_mlf_core: dict or None):
        """ Prompts for mlflow-xgboost_dask specific options and saves them into the MlflowTemplateStruct """
        pass
