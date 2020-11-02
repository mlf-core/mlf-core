import os
import shutil


def remove(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)


xgboost_files = ['{{ cookiecutter.project_slug_no_hyphen }}/{{ cookiecutter.project_slug_no_hyphen }}/cli_xgboost.py',
                 '{{ cookiecutter.project_slug_no_hyphen }}/{{ cookiecutter.project_slug_no_hyphen }}/data/xgboost_test_data.tsv',
                 '{{ cookiecutter.project_slug_no_hyphen }}/{{ cookiecutter.project_slug_no_hyphen }}/models/xgboost_test_model.xgb']

is_pytorch = '{{ cookiecutter.framework }}' == 'pytorch'
is_tensorflow = '{{ cookiecutter.framework }}' == 'tensorflow'
is_xgboost = '{{ cookiecutter.framework }}' == 'xgboost'

if not is_pytorch:
    pass

if not is_tensorflow:
    pass

if not is_xgboost:
    for file in xgboost_files:
        remove(os.path.join(os.getcwd(), file))
