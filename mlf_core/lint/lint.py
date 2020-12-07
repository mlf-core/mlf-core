import sys
from pathlib import Path
from ruamel.yaml import YAML
from rich import print

from mlf_core.lint.domains.mlflow import MlflowPytorchLint, MlflowTensorflowLint, MlflowXGBoostLint, MlflowXGBoostDaskLint
from mlf_core.lint.domains.package import PackagePredictionLint
from mlf_core.lint.template_linter import TemplateLinter


def lint_project(project_dir: str) -> TemplateLinter:
    """
    Verifies the integrity of a project to best coding and practices.
    Runs a set of general linting functions, which all templates share and afterwards runs template specific linting functions.
    All results are collected and presented to the user.
    """
    # Detect which template the project is based on
    template_handle = get_template_handle(project_dir)

    switcher = {
        'mlflow-pytorch': MlflowPytorchLint,
        'mlflow-tensorflow': MlflowTensorflowLint,
        'mlflow-xgboost': MlflowXGBoostLint,
        'mlflow-xgboost_dask': MlflowXGBoostDaskLint,
        'package-prediction': PackagePredictionLint
    }

    try:
        lint_obj = switcher.get(template_handle)(project_dir)
    except TypeError:
        print(f'[bold red]Unable to find linter for handle {template_handle}! Aborting...')
        sys.exit(1)

    # Run the linting tests
    try:
        # Run non project specific linting
        print('[bold blue]Running general linting')
        lint_obj.lint_project(super(lint_obj.__class__, lint_obj), is_subclass_calling=False)

        # Run the project specific linting
        print(f'[bold blue]Running {template_handle} linting')

        lint_obj.lint()
    except AssertionError as e:
        print(f'[bold red]Critical error: {e}')
        print('[bold red] Stopping tests...')

        return lint_obj

    # Print the results
    lint_obj._print_results()

    # Exit code
    if len(lint_obj.failed) > 0:
        print(f'[bold red] {len(lint_obj.failed)} tests failed! Exiting with non-zero error code.')
        sys.exit(1)


def get_template_handle(dot_mlf_core_path: str = '.mlf_core.yml') -> str:
    """
    Reads the .mlf_core file and extracts the template handle
    :param dot_mlf_core_path: path to the .mlf_core file
    :return: found template handle
    """
    path = Path(f'{dot_mlf_core_path}/.mlf_core.yml')
    if not path.exists():
        print('[bold red].mlf_core.yml not found. Is this a mlf-core project?')
        sys.exit(1)
    yaml = YAML(typ='safe')
    dot_mlf_core_content = yaml.load(path)

    return dot_mlf_core_content['template_handle']
