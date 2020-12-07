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
            '.github/workflows/train_cpu.yml',
            '.github/workflows/run_flake8_linting.yml',
            '.github/workflows/run_bandit.yml',
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
            [f'{self.project_slug_no_hyphen}/mlf_core/mlf_core.py']
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
        entry_point_file_path = f'{self.path}/{self.project_slug_no_hyphen}/{self.project_slug_no_hyphen}.py'
        with open(entry_point_file_path) as f:
            project_slug_entry_point_content = list(map(lambda line: line.strip(), f.readlines()))

        expected_lines_pytorch_reproducibility = ['def set_pytorch_random_seeds(seed, use_cuda):',
                                                  'torch.manual_seed(seed)',
                                                  'torch.cuda.manual_seed(seed)',
                                                  'torch.cuda.manual_seed_all(seed)  # For multiGPU',
                                                  'torch.backends.cudnn.deterministic = True',
                                                  'torch.backends.cudnn.benchmark = False',
                                                  'set_general_random_seeds(general_seed)',
                                                  'set_pytorch_random_seeds(pytorch_seed, use_cuda=use_cuda)']

        for expected_line in expected_lines_pytorch_reproducibility:
            if expected_line not in project_slug_entry_point_content:
                passed_pytorch_reproducibility_seeds = False
                self.failed.append(('mlflow-pytorch-2', f'{expected_line} not found in {entry_point_file_path}'))

        if passed_pytorch_reproducibility_seeds:
            self.passed.append(('mlflow-pytorch-2', 'All required reproducibility settings enabled.'))

    def pytorch_no_atomic_operations(self) -> None:
        """
        Verifies that the project does not use any of the potentially non-deterministic atomicAdd functions.

        There are some PyTorch functions that use CUDA functions that can be a source of nondeterminism.
        One class of such CUDA functions are atomic operations, in particular atomicAdd, which can lead to the order of additions being nondetermnistic.
        Because floating-point addition is not perfectly associative for floating-point operands,
        atomicAdd with floating-point operands can introduce different floating-point rounding errors on each evaluation,
        which introduces a source of nondeterministic variance (aka noise) in the result.
        PyTorch functions that use atomicAdd in the forward kernels include torch.Tensor.index_add_(), torch.Tensor.scatter_add_(), torch.bincount().
        A number of operations have backwards kernels that use atomicAdd, including torch.nn.functional.embedding_bag(),
        torch.nn.functional.ctc_loss(), torch.nn.functional.interpolate(), and many forms of pooling, padding, and sampling.
        There is currently no simple way of avoiding nondeterminism in these functions.
        Additionally, the backward path for repeat_interleave() operates nondeterministically on the CUDA backend because repeat_interleave() is implemented
        using index_select(), the backward path for which is implemented using index_add_(), which is known to operate
        nondeterministically (in the forward direction) on the CUDA backend (see above).

        Source: https://pytorch.org/docs/stable/notes/randomness.html
        """
        atomic_add_functions = [
            'index_add',
            'scatter_add',
            'bincount',
            'embedding_bag',
            'ctc_loss',
            'interpolate',
            'repeat_interleave',
            'index_select'
        ]

        verify_method_not_present(self, atomic_add_functions, 'mlflow-pytorch-3')

        # TODO COOKIETEMPLE: Add all functions to atomic_add_functions, which also use these methods.


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
            'MLproject,
            'environment.yml',
            'project_slug_no_hyphen/mlf_core/mlf_core.py',
        Files that *should* be present::
            '.github/workflows/train_cpu.yml',
            '.github/workflows/run_flake8_linting.yml',
            '.github/workflows/run_bandit.yml',
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
            [f'{self.project_slug_no_hyphen}/mlf_core/mlf_core.py']
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
        entry_point_file_path = f'{self.path}/{self.project_slug_no_hyphen}/{self.project_slug_no_hyphen}.py'
        with open(entry_point_file_path) as f:
            project_slug_entry_point_content = list(map(lambda line: line.strip(), f.readlines()))

        expected_lines_pytorch_reproducibility = ['def set_tensorflow_random_seeds(seed):',
                                                  'tf.random.set_seed(seed)',
                                                  'tf.config.threading.set_intra_op_parallelism_threads = 1  # CPU only',
                                                  'tf.config.threading.set_inter_op_parallelism_threads = 1  # CPU only',
                                                  'os.environ[\'TF_DETERMINISTIC_OPS\'] = \'1\'',
                                                  'set_general_random_seeds(general_seed)',
                                                  'set_tensorflow_random_seeds(tensorflow_seed)']

        for expected_line in expected_lines_pytorch_reproducibility:
            if expected_line not in project_slug_entry_point_content:
                passed_tensorflow_reproducibility_seeds = False
                self.failed.append(('mlflow-tensorflow-2', f'{expected_line} not found in {entry_point_file_path}'))

        if passed_tensorflow_reproducibility_seeds:
            self.passed.append(('mlflow-tensorflow-2', 'All required reproducibility settings enabled.'))

        # TODO COOKIETEMPLE: Investigate whether there is a reasonable way of linting for
        # train_dataset = mnist_train.map(scale).cache().shuffle(buffer_size, seed=tensorflow_seed, reshuffle_each_iteration=False).batch(BATCH_SIZE)

    def tensorflow_non_deterministic_functions(self) -> None:
        """
        Verifies that no non-deterministic functions of Tensorflow are used.
        """
        non_deterministic_tf_functions = ['softmax_cross_entropy_with_logits',
                                          'sparse_softmax_cross_entropy_with_logits']

        verify_method_not_present(self, non_deterministic_tf_functions, 'mlflow-tensorflow-3')


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
            [f'{self.project_slug_no_hyphen}/mlf_core/mlf_core.py']
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
        entry_point_file_path = f'{self.path}/{self.project_slug_no_hyphen}/{self.project_slug_no_hyphen}.py'
        with open(entry_point_file_path) as f:
            project_slug_entry_point_content = list(map(lambda line: line.strip(), f.readlines()))

        expected_lines_xgboost_reproducibility = ['def set_xgboost_random_seeds(seed, param):',
                                                  'param[\'seed\'] = seed',
                                                  'set_general_random_seeds(general_seed)',
                                                  'set_xgboost_random_seeds(xgboost_seed, param)']

        for expected_line in expected_lines_xgboost_reproducibility:
            if expected_line not in project_slug_entry_point_content:
                passed_xgboost_reproducibility_seeds = False
                self.failed.append(('mlflow-xgboost-2', f'{expected_line} not found in {entry_point_file_path}'))

        if passed_xgboost_reproducibility_seeds:
            self.passed.append(('mlflow-xgboost-2', 'All required reproducibility settings enabled.'))

    def xgboost_version(self) -> None:
        """
        Verifies that the XGBoost version is at least 1.1.0, since reproducibility cannot be guaranteed elsewise.
        """
        # Verify that XGBoost version is greater than 1.1.0
        conda_env = load_yaml_file(f'{self.path}/environment.yml')
        conda_only = list(filter(lambda dep: '::' in dep, conda_env['dependencies']))
        pip_only = list(filter(lambda dep: isinstance(dep, dict), conda_env['dependencies']))[0]['pip']

        for dependency in conda_only:
            if 'xgboost' in dependency:
                split = dependency.split('==')
                current_version = parse_version(split[-1])
                if current_version < parse_version('1.1.0'):
                    self.failed.append(('mlflow-xgboost-3',
                                        f'XGBoost version {current_version} is not at least 1.1.0. Reproducibility cannot be guaranteed.'))

        for dependency in pip_only:
            if 'xgboost' in dependency:
                split = dependency.split('==')
                current_version = parse_version(split[-1])
                if current_version < parse_version('1.1.0'):
                    self.failed.append(('mlflow-xgboost-3',
                                        f'XGBoost version {current_version} is not at least 1.1.0. Reproducibility cannot be guaranteed.'))

    def xgboost_no_all_reduce(self) -> None:
        """
        Verifies that all_reduce is not used.
        https://github.com/dmlc/xgboost/issues/5023
        """
        all_reduce_functions = ['all_reduce']
        verify_method_not_present(self, all_reduce_functions, 'mlflow-xgboost-4')


class MlflowXGBoostDaskLint(TemplateLinter, metaclass=GetLintingFunctionsMeta):
    def __init__(self, path):
        super().__init__(path)

    def lint(self):
        super().lint_project(self, self.methods)

    def xgboost_dask_files_exist(self) -> None:
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
            [f'{self.project_slug_no_hyphen}/mlf_core/mlf_core.py']
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
        entry_point_file_path = f'{self.path}/{self.project_slug_no_hyphen}/{self.project_slug_no_hyphen}.py'
        with open(entry_point_file_path) as f:
            project_slug_entry_point_content = list(map(lambda line: line.strip(), f.readlines()))

        expected_lines_xgboost_reproducibility = ['def set_xgboost_dask_random_seeds(seed, param):',
                                                  'param[\'seed\'] = seed',
                                                  'set_general_random_seeds(general_seed)',
                                                  'set_xgboost_dask_random_seeds(xgboost_seed, param)']

        for expected_line in expected_lines_xgboost_reproducibility:
            if expected_line not in project_slug_entry_point_content:
                passed_xgboost_reproducibility_seeds = False
                self.failed.append(('mlflow-xgboost_dask-2', f'{expected_line} not found in {entry_point_file_path}'))

        if passed_xgboost_reproducibility_seeds:
            self.passed.append(('mlflow-xgboost_dask-2', 'All required reproducibility settings enabled.'))

    def xgboost_version(self) -> None:
        """
        Verifies that the XGBoost version is at least 1.1.0, since reproducibility cannot be guaranteed elsewise.
        """
        # Verify that XGBoost version is greater than 1.1.0
        conda_env = load_yaml_file(f'{self.path}/environment.yml')
        conda_only = list(filter(lambda dep: '::' in dep, conda_env['dependencies']))
        pip_only = list(filter(lambda dep: isinstance(dep, dict), conda_env['dependencies']))[0]['pip']

        for dependency in conda_only:
            if 'xgboost' in dependency:
                split = dependency.split('==')
                current_version = parse_version(split[-1])
                if current_version < parse_version('1.1.0'):
                    self.failed.append(('mlflow-xgboost_dask-3',
                                        f'XGBoost version {current_version} is not at least 1.1.0. Reproducibility cannot be guaranteed.'))

        for dependency in pip_only:
            if 'xgboost' in dependency:
                split = dependency.split('==')
                current_version = parse_version(split[-1])
                if current_version < parse_version('1.1.0'):
                    self.failed.append(('mlflow-xgboost_dask-3',
                                        f'XGBoost version {current_version} is not at least 1.1.0. Reproducibility cannot be guaranteed.'))

    def xgboost_no_all_reduce(self) -> None:
        """
        Verifies that all_reduce is not used.
        https://github.com/dmlc/xgboost/issues/5023
        """
        all_reduce_functions = ['all_reduce']
        verify_method_not_present(self, all_reduce_functions, 'mlflow-xgboost-4')


def verify_method_not_present(calling_class: TemplateLinter, functions_to_check: list, linting_code: str):
    """
    Checks all Python files for a list of strings/functions, which should not be present.
    :param calling_class: The TemplateLinter subclass. Required to append the found errors correctly.
    :param functions_to_check: The list of functions, which are not allowed to be present in any Python file
    :param linting_code: A linting code build from the handle and the error code e.g. mlflow-pytorch-1
    """
    # We should only expect those functions in all *.py files, so only read those
    for root, dirs, files in os.walk(f'{calling_class.path}/{calling_class.project_slug_no_hyphen}'):
        for file in files:
            if file.endswith(".py"):
                file_to_check_full_path = os.path.join(root, file)
                with open(file_to_check_full_path) as f:
                    content_stripped = list(map(lambda line: line.strip(), f.readlines()))
                    for function in functions_to_check:
                        for line_code in content_stripped:
                            if function in line_code:
                                calling_class.failed.append((linting_code,
                                                             f'{function} found in {file_to_check_full_path} operates non-deterministically.'))
