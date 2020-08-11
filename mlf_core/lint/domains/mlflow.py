import os

from pkg_resources import parse_version

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
            'MLproject',
            'environment.yml',
            'project_slug/'
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
            [f'{self.project_slug}/mlf_core/mlf_core.py']
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

    def pytorch_reproducibility_seeds(self) -> None:
        """
        Verifies that all CPU and GPU reproducibility settings for Pytorch are enabled
        Required are:
        def set_pytorch_random_seeds(seed, use_cuda):
            torch.manual_seed(seed)
            if use_cuda:
                torch.cuda.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)  # For multiGPU
                torch.backends.cudnn.deterministic = True
                torch.backends.cudnn.benchmark = False
        """
        passed_pytorch_reproducibility_seeds = True
        entry_point_file_path = f'{self.path}/{self.project_slug}/{self.project_slug}.py'
        with open(entry_point_file_path) as f:
            project_slug_entry_point_content = list(map(lambda line: line.strip(), f.readlines()))

        expected_lines_pytorch_reproducibility = ['def set_pytorch_random_seeds(seed, use_cuda):',
                                                  'torch.manual_seed(seed)',
                                                  'torch.cuda.manual_seed(seed)',
                                                  'torch.cuda.manual_seed_all(seed)  # For multiGPU',
                                                  'torch.backends.cudnn.deterministic = True',
                                                  'torch.backends.cudnn.benchmark = False',
                                                  'set_general_random_seeds(general_seed)',
                                                  'set_pytorch_random_seeds(pytorch_seed, use_cuda=use_cuda)',
                                                  f'log_sys_intel_conda_env(\'{self.project_slug}\')']

        for expected_line in expected_lines_pytorch_reproducibility:
            if expected_line not in project_slug_entry_point_content:
                passed_pytorch_reproducibility_seeds = False
                self.failed.append(('mlflow-pytorch-2', f'{expected_line} not found in {entry_point_file_path}'))

        if passed_pytorch_reproducibility_seeds:
            self.passed.append(('mlflow-pytorch-2', 'All required reproducibility settings enabled.'))


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
            [f'{self.project_slug}/mlf_core/mlf_core.py']
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

    def tensorflow_reproducibility_seeds(self) -> None:
        """
        Verifies that all CPU and GPU reproducibility settings for Tensorflow are enabled
        Required are:
        def set_tensorflow_random_seeds(seed):
            tf.random.set_seed(seed)
            tf.config.threading.set_intra_op_parallelism_threads = 1  # CPU only -> https://github.com/NVIDIA/tensorflow-determinism
            tf.config.threading.set_inter_op_parallelism_threads = 1  # CPU only
            os.environ['TF_DETERMINISTIC_OPS'] = '1'
        """
        passed_tensorflow_reproducibility_seeds = True
        entry_point_file_path = f'{self.path}/{self.project_slug}/{self.project_slug}.py'
        with open(entry_point_file_path) as f:
            project_slug_entry_point_content = list(map(lambda line: line.strip(), f.readlines()))

        expected_lines_pytorch_reproducibility = ['def set_tensorflow_random_seeds(seed):',
                                                  'tf.random.set_seed(seed)',
                                                  'tf.config.threading.set_intra_op_parallelism_threads = 1  # CPU only',
                                                  'tf.config.threading.set_inter_op_parallelism_threads = 1  # CPU only',
                                                  'os.environ[\'TF_DETERMINISTIC_OPS\'] = \'1\'',
                                                  'set_general_random_seeds(general_seed)',
                                                  'set_tensorflow_random_seeds(tensorflow_seed)',
                                                  f'log_sys_intel_conda_env(\'{self.project_slug}\')']

        for expected_line in expected_lines_pytorch_reproducibility:
            if expected_line not in project_slug_entry_point_content:
                passed_tensorflow_reproducibility_seeds = False
                self.failed.append(('mlflow-tensorflow-2', f'{expected_line} not found in {entry_point_file_path}'))

        if passed_tensorflow_reproducibility_seeds:
            self.passed.append(('mlflow-tensorflow-2', 'All required reproducibility settings enabled.'))

        # TODO COOKIETEMPLE: Investigate whether there is a reasonable way of linting for
        # train_dataset = mnist_train.map(scale).cache().shuffle(buffer_size, seed=tensorflow_seed, reshuffle_each_iteration=False).batch(BATCH_SIZE)


class MlflowXGBoostLint(TemplateLinter, metaclass=GetLintingFunctionsMeta):
    def __init__(self, path):
        super().__init__(path)

    def lint(self):
        super().lint_project(self, self.methods)

    def xgboost_files_exist(self) -> None:
        """
        Checks a given project directory for required files.
        Iterates through the templates's directory content and checkmarks files for presence.
        Files that **must** be present::
            'MLproject',
            'environment.yml',
            'project_slug/mlf_core/mlf_core.py'
        Files that *should* be present::
            '.github/workflows/train_cpu.yml',
            '.github/workflows/run_bandit.yml',
            '.github/workflows/run_flake8_linting.yml',
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
            [f'{self.project_slug}/mlf_core/mlf_core.py']
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

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle='mlflow-xgboost')

    def xgboost_reproducibility_seeds(self) -> None:
        """
        Verifies that all CPU and GPU reproducibility settings for XGBoost are enabled
        Required are:
        def set_pytorch_random_seeds(seed, use_cuda):
            torch.manual_seed(seed)
            if use_cuda:
                torch.cuda.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)  # For multiGPU
                torch.backends.cudnn.deterministic = True
                torch.backends.cudnn.benchmark = False
        """
        passed_xgboost_reproducibility_seeds = True
        entry_point_file_path = f'{self.path}/{self.project_slug}/{self.project_slug}.py'
        with open(entry_point_file_path) as f:
            project_slug_entry_point_content = list(map(lambda line: line.strip(), f.readlines()))

        expected_lines_xgboost_reproducibility = ['def set_xgboost_random_seeds(seed, param):',
                                                  'param[\'seed\'] = seed',
                                                  'set_general_random_seeds(general_seed)',
                                                  'set_xgboost_random_seeds(xgboost_seed, param)',
                                                  f'log_sys_intel_conda_env(\'{self.project_slug}\')']

        for expected_line in expected_lines_xgboost_reproducibility:
            if expected_line not in project_slug_entry_point_content:
                passed_xgboost_reproducibility_seeds = False
                self.failed.append(('mlflow-xgboost-2', f'{expected_line} not found in {entry_point_file_path}'))

        # Verify that XGBoost version is greater than 1.1.0
        conda_env = load_yaml_file(f'{self.path}/environment.yml')
        conda_only = list(filter(lambda dep: '::' in dep, conda_env['dependencies']))
        pip_only = list(filter(lambda dep: isinstance(dep, dict), conda_env['dependencies']))[0]['pip']

        for dependency in conda_only:
            if 'xgboost' in dependency:
                split = dependency.split('==')
                current_version = parse_version(split[-1])
                if current_version < parse_version('1.1.0'):
                    self.failed.append(('mlflow-xgboost-2', f'XGBoost version {current_version} is not at least 1.1.0. Reproducibility cannot be guaranteed.'))

        for dependency in pip_only:
            if 'xgboost' in dependency:
                split = dependency.split('==')
                current_version = parse_version(split[-1])
                if current_version < parse_version('1.1.0'):
                    self.failed.append(('mlflow-xgboost-2', f'XGBoost version {current_version} is not at least 1.1.0. Reproducibility cannot be guaranteed.'))

        if passed_xgboost_reproducibility_seeds:
            self.passed.append(('mlflow-xgboost-2', 'All required reproducibility settings enabled.'))


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
            'MLproject',
            'environment.yml',
            'project_slug/mlf_core/mlf_core.py'
        Files that *should* be present::
            '.github/workflows/train_cpu.yml',
            '.github/workflows/run_bandit.yml',
            '.github/workflows/run_flake8_linting.yml',
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
            [f'{self.project_slug}/mlf_core/mlf_core.py']
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

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle='mlflow-xgboost_dask')

    def xgboost_reproducibility_seeds(self) -> None:
        """
        Verifies that all CPU and GPU reproducibility settings for XGBoost are enabled
        Required are:
        def set_pytorch_random_seeds(seed, use_cuda):
            torch.manual_seed(seed)
            if use_cuda:
                torch.cuda.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)  # For multiGPU
                torch.backends.cudnn.deterministic = True
                torch.backends.cudnn.benchmark = False
        """
        passed_xgboost_reproducibility_seeds = True
        entry_point_file_path = f'{self.path}/{self.project_slug}/{self.project_slug}.py'
        with open(entry_point_file_path) as f:
            project_slug_entry_point_content = list(map(lambda line: line.strip(), f.readlines()))

        expected_lines_xgboost_reproducibility = ['def set_xgboost_dask_random_seeds(seed, param):',
                                                  'param[\'seed\'] = seed',
                                                  'set_general_random_seeds(general_seed)',
                                                  'set_xgboost_dask_random_seeds(xgboost_seed, param)',
                                                  f'log_sys_intel_conda_env(\'{self.project_slug}\')']

        for expected_line in expected_lines_xgboost_reproducibility:
            if expected_line not in project_slug_entry_point_content:
                passed_xgboost_reproducibility_seeds = False
                self.failed.append(('mlflow-xgboost-2', f'{expected_line} not found in {entry_point_file_path}'))

        # Verify that XGBoost version is greater than 1.1.0
        conda_env = load_yaml_file(f'{self.path}/environment.yml')
        conda_only = list(filter(lambda dep: '::' in dep, conda_env['dependencies']))
        pip_only = list(filter(lambda dep: isinstance(dep, dict), conda_env['dependencies']))[0]['pip']

        for dependency in conda_only:
            if 'xgboost' in dependency:
                split = dependency.split('==')
                current_version = parse_version(split[-1])
                if current_version < parse_version('1.1.0'):
                    self.failed.append(('mlflow-xgboost-2', f'XGBoost version {current_version} is not at least 1.1.0. Reproducibility cannot be guaranteed.'))

        for dependency in pip_only:
            if 'xgboost' in dependency:
                split = dependency.split('==')
                current_version = parse_version(split[-1])
                if current_version < parse_version('1.1.0'):
                    self.failed.append(('mlflow-xgboost-2', f'XGBoost version {current_version} is not at least 1.1.0. Reproducibility cannot be guaranteed.'))

        if passed_xgboost_reproducibility_seeds:
            self.passed.append(('mlflow-xgboost-2', 'All required reproducibility settings enabled.'))
