import os
import shutil


def remove(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)


cli_path = '{{ cookiecutter.project_slug_no_hyphen }}/{{ cookiecutter.project_slug_no_hyphen }}'

pytorch_files = [f'{cli_path}/cli_pytorch.py']

tensorflow_files = [f'{cli_path}/cli_tensorflow.py']

xgboost_files = [f'{cli_path}/cli_xgboost.py',
                 '{{ cookiecutter.project_slug_no_hyphen }}/data/xgboost_test_data.tsv',
                 '{{ cookiecutter.project_slug_no_hyphen }}/models/xgboost_test_model.xgb']

is_pytorch = '{{ cookiecutter.framework }}' == 'pytorch'
is_tensorflow = '{{ cookiecutter.framework }}' == 'tensorflow'
is_xgboost = '{{ cookiecutter.framework }}' == 'xgboost'

if not is_pytorch:
    for file in pytorch_files:
        remove(os.path.join(os.getcwd(), file))

if not is_tensorflow:
    for file in tensorflow_files:
        remove(os.path.join(os.getcwd(), file))

if not is_xgboost:
    for file in xgboost_files:
        remove(os.path.join(os.getcwd(), file))
