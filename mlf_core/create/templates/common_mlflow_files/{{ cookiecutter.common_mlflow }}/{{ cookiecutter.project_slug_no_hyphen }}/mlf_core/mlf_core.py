import tempfile
import os
import numpy as np
import random
import subprocess
from rich import print
{%- if cookiecutter.language == "pytorch" %}
import torch
import mlflow.pytorch
{%- elif cookiecutter.language == "tensorflow" %}
# ONLY FOR TENSORFLOW -> else RuntimeError: make_default_context() wasn't able to create a context on any of the 1 detected devices
import tensorflow as tf
from system_intelligence.query import query_and_export  # noqa F401
{%- endif %}


class MLFCore:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            print('Creating the object')
            cls._instance = super(MLFCore, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    @staticmethod
    def set_general_random_seeds(seed):
        os.environ['PYTHONHASHSEED'] = str(seed)  # Python general
        np.random.seed(seed)  # Numpy random
        random.seed(seed)  # Python random

    @staticmethod
    def log_system_intelligence(reports_output_dir: str):
        # Scoped import to prevent issues like RuntimeError: Numba cannot operate on non-primary CUDA context
        from system_intelligence.query import query_and_export

        print(f'[bold blue]Writing reports locally to {reports_output_dir}\n')
        print('[bold blue]Running system-intelligence')
        query_and_export(query_scope={'all'},
                         verbose=False,
                         export_format='json',
                         generate_html_table=True,
                         output=f'{reports_output_dir}/system_intelligence.json')
        print('[bold blue]Uploading system-intelligence report as a run artifact...')
        mlflow.log_artifacts(reports_output_dir, artifact_path='reports')

    @staticmethod
    def log_conda_environment(reports_output_dir: str):
        print('[bold blue]Exporting conda environment...')
        conda_env_filehandler = open(f'{reports_output_dir}/{{ cookiecutter.project_slug_no_hyphen }}_conda_environment.yml', 'w')
        subprocess.call(['conda', 'env', 'export', '--name', '{{ cookiecutter.project_slug_no_hyphen }}'], stdout=conda_env_filehandler)
        print('[bold blue]Uploading conda environment report as a run artifact...')
        mlflow.log_artifact(f'{reports_output_dir}/{{ cookiecutter.project_slug_no_hyphen }}_conda_environment.yml', artifact_path='reports')

{%- if cookiecutter.language == "pytorch" %}

    @staticmethod
    def set_pytorch_random_seeds(seed, num_gpus):
        torch.manual_seed(seed)
        if num_gpus > 0:
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)  # For multiGPU

{%- elif cookiecutter.language == "tensorflow" %}

    @staticmethod
    def set_tensorflow_random_seeds(seed):
        tf.random.set_seed(seed)
        tf.config.threading.set_intra_op_parallelism_threads = 1  # CPU only
        tf.config.threading.set_inter_op_parallelism_threads = 1  # CPU only
        os.environ['TF_DETERMINISTIC_OPS'] = '1'

{%- elif cookiecutter.language == "xgboost" %}

    @staticmethod
    def set_xgboost_random_seeds(seed, param):
        param['seed'] = seed

{%- elif cookiecutter.language == "xgboost_dask" %}

    @staticmethod
    def set_xgboost_dask_random_seeds(seed, param):
        param['seed'] = seed

{%- endif %}

    @classmethod
    def log_sys_intel_conda_env(cls):
        reports_output_dir = tempfile.mkdtemp()
        cls.log_system_intelligence(reports_output_dir)
        cls.log_conda_environment(reports_output_dir)
