import os

from mlf_core.common.load_yaml import load_yaml_file
from mlf_core.lint.template_linter import TemplateLinter, files_exist_linting, GetLintingFunctionsMeta

CWD = os.getcwd()


class MlflowPytorchLint(TemplateLinter, metaclass=GetLintingFunctionsMeta):
    def __init__(self, path):
        super().__init__(path)

    def lint(self):
        super().lint_project(self, self.methods)

    def pytorch_files_exist(self) -> None:
        """
        Checks a given project directory for required files.
        Iterates through the templates's directory content and checkmarks files for presence.
        Files that **must** be present::
            'setup.py',
            'setup.cfg',
            'MANIFEST.in',
            'tox.ini',
        Files that *should* be present::
            '.github/workflows/build_package.yml',
            '.github/workflows/publish_package.yml',
            '.github/workflows/tox_testsuite.yml',
            '.github/workflows/flake8.yml',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            '__pycache__'
        """

        # NB: Should all be files, not directories
        # List of lists. Passes if any of the files in the sublist are found.
        files_fail = [
            ['MLproject'],
            ['environment.yml'],
        ]
        files_warn = [
            [os.path.join('.github', 'workflows', 'train_cpu.yml')],
            [os.path.join('.github', 'workflows', 'run_flake8_linting.yml')],
            [os.path.join('.github', 'workflows', 'run_bandit.yml')],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [
            '__pycache__'
        ]
        files_warn_ifexists = [

        ]

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle='mlflow-pytorch')

    def check_conda_environment(self) -> None:
        passed_conda_check = True
        conda_env = load_yaml_file(f'{self.path}/environment.yml')

        # Verify that the structure is somewhat reasonable
        for section in ['name', 'channels', 'dependencies']:
            if section not in conda_env:
                passed_conda_check = False
                self.failed.append(('mlflow-pytorch-2', f'Section {section} missing from environment.yml file!'))

        # Verify that all Conda dependencies have a pinned version number
        conda_only = list(filter(lambda dependency: '::' in dependency, conda_env['dependencies']))
        for dependency in conda_only:
            dependency_name, dependency_version = dependency.split('=')[:2]
            if not dependency_version:
                passed_conda_check = False
                self.failed.append(('mlflow-pytorch-2', f'Dependency {dependency} does not have a pinned version!'))

        # Verify that all Conda dependencies are up to date
        for dependency in conda_only:
            self._check_anaconda_package(dependency, conda_env)

        if passed_conda_check:
            self.passed.append(('mlflow-pytorch-2', 'Passed conda environment checks.'))


class MlflowTensorflowLint(TemplateLinter, metaclass=GetLintingFunctionsMeta):
    def __init__(self, path):
        super().__init__(path)

    def lint(self):
        super().lint_project(self, self.methods)

    def tensorflow_files_exist(self) -> None:
        """
        Checks a given project directory for required files.
        Iterates through the templates's directory content and checkmarks files for presence.
        Files that **must** be present::
            'setup.py',
            'setup.cfg',
            'MANIFEST.in',
            'tox.ini',
        Files that *should* be present::
            '.github/workflows/build_package.yml',
            '.github/workflows/publish_package.yml',
            '.github/workflows/tox_testsuite.yml',
            '.github/workflows/flake8.yml',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            '__pycache__'
        """

        # NB: Should all be files, not directories
        # List of lists. Passes if any of the files in the sublist are found.
        files_fail = [
            ['MLproject'],
            ['environment.yml'],
        ]
        files_warn = [
            [os.path.join('.github', 'workflows', 'train_cpu.yml')],
            [os.path.join('.github', 'workflows', 'run_flake8_linting.yml')],
            [os.path.join('.github', 'workflows', 'run_bandit.yml')],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [
            '__pycache__'
        ]
        files_warn_ifexists = [

        ]

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle='mlflow-tensorflow')


class MlflowXGBoostLint(TemplateLinter, metaclass=GetLintingFunctionsMeta):
    def __init__(self, path):
        super().__init__(path)

    def lint(self):
        super().lint_project(self, self.methods)

    def tensorflow_files_exist(self) -> None:
        """
        Checks a given project directory for required files.
        Iterates through the templates's directory content and checkmarks files for presence.
        Files that **must** be present::
            'setup.py',
            'setup.cfg',
            'MANIFEST.in',
            'tox.ini',
        Files that *should* be present::
            '.github/workflows/build_package.yml',
            '.github/workflows/publish_package.yml',
            '.github/workflows/tox_testsuite.yml',
            '.github/workflows/flake8.yml',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            '__pycache__'
        """

        # NB: Should all be files, not directories
        # List of lists. Passes if any of the files in the sublist are found.
        files_fail = [
            ['MLproject'],
            ['environment.yml'],
        ]
        files_warn = [
            [os.path.join('.github', 'workflows', 'train_cpu.yml')],
            [os.path.join('.github', 'workflows', 'run_flake8_linting.yml')],
            [os.path.join('.github', 'workflows', 'run_bandit.yml')],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [
            '__pycache__'
        ]
        files_warn_ifexists = [

        ]

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle='mlflow-tensorflow')


class MlflowXGBoostDaskLint(TemplateLinter, metaclass=GetLintingFunctionsMeta):
    def __init__(self, path):
        super().__init__(path)

    def lint(self):
        super().lint_project(self, self.methods)

    def tensorflow_files_exist(self) -> None:
        """
        Checks a given project directory for required files.
        Iterates through the templates's directory content and checkmarks files for presence.
        Files that **must** be present::
            'setup.py',
            'setup.cfg',
            'MANIFEST.in',
            'tox.ini',
        Files that *should* be present::
            '.github/workflows/build_package.yml',
            '.github/workflows/publish_package.yml',
            '.github/workflows/tox_testsuite.yml',
            '.github/workflows/flake8.yml',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            '__pycache__'
        """

        # NB: Should all be files, not directories
        # List of lists. Passes if any of the files in the sublist are found.
        files_fail = [
            ['MLproject'],
            ['environment.yml'],
        ]
        files_warn = [
            [os.path.join('.github', 'workflows', 'train_cpu.yml')],
            [os.path.join('.github', 'workflows', 'run_flake8_linting.yml')],
            [os.path.join('.github', 'workflows', 'run_bandit.yml')],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [
            '__pycache__'
        ]
        files_warn_ifexists = [

        ]

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle='mlflow-tensorflow')
