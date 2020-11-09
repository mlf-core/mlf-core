import platform

import click
import tempfile
import mlflow
import subprocess
import os
import numpy as np
import random
# ONLY FOR TENSORFLOW -> else RuntimeError: make_default_context() wasn't able to create a context on any of the 1 detected devices
from system_intelligence.query import query_and_export  # noqa F401


def set_general_random_seeds(seed):
    os.environ['PYTHONHASHSEED'] = str(seed)  # Python general
    np.random.seed(seed)  # Numpy random
    random.seed(seed)  # Python random


def log_sys_intel_conda_env():
    reports_output_dir = tempfile.mkdtemp()
    log_system_intelligence(reports_output_dir)
    log_conda_environment(reports_output_dir)


def log_system_intelligence(reports_output_dir: str):
    current_platform = platform.system()
    if current_platform != 'Linux':
        click.echo(click.style(f'Running on {current_platform} which is not supported by system-intelligence. Skipping hardware report.', fg='red'))
        click.echo(click.style('Run MLflow with Docker to enforce a Linux environment.', fg='blue'))
        return

    # Scoped import to prevent issues like RuntimeError: Numba cannot operate on non-primary CUDA context
    from system_intelligence.query import query_and_export  # noqa F811

    click.echo(click.style(f'Writing reports locally to {reports_output_dir}\n', fg='blue'))
    click.echo(click.style('Running system-intelligence', fg='blue'))
    query_and_export(query_scope=list(('all',)),
                     verbose=False,
                     export_format='json',
                     generate_html_table=True,
                     output=f'{reports_output_dir}/system_intelligence.json')
    click.echo(click.style('Uploading system-intelligence report as a run artifact...', fg='blue'))
    mlflow.log_artifacts(reports_output_dir, artifact_path='reports')


def log_conda_environment(reports_output_dir: str):
    click.echo(click.style('Exporting conda environment...', fg='blue'))
    conda_env_filehandler = open(f'{reports_output_dir}/{{ cookiecutter.project_slug_no_hyphen }}_conda_environment.yml', "w")
    subprocess.call(['conda', 'env', 'export', '--name', '{{ cookiecutter.project_slug_no_hyphen }}'], stdout=conda_env_filehandler)
    click.echo(click.style('Uploading conda environment report as a run artifact...', fg='blue'))
    mlflow.log_artifact(f'{reports_output_dir}/{{ cookiecutter.project_slug_no_hyphen }}_conda_environment.yml', artifact_path='reports')
