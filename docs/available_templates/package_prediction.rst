package-prediction
-------------------

Purpose
^^^^^^^^

package-prediction is a template designed to easily distribute `PyPI <https://pypi.org/>`_ packages of machine learning models.
The template only provides the boilerplate code to load models and perform predictions. Data wrangling or model training should be done using the mlflow templates.

Design
^^^^^^^^

The package is closely related to `<cookietemple's https://github.com/cookiejar/cookietemple>`_ `cli-python <https://cookietemple.readthedocs.io/en/latest/available_templates/available_templates.html#cli-python>`_ template.
It is primarily based on setuptools to build the package and uses a Github workflow to easily upload the package to `PyPI <https://pypi.org/>`_.
Any prediction boiler code is machine learning library specific.

.. code::

    ├── AUTHORS.rst
    ├── .bandit.yml
    ├── CHANGELOG.rst
    ├── CODE_OF_CONDUCT.rst
    ├── .coveragerc
    ├── Dockerfile
    ├── docs
    │   ├── authors.rst
    │   ├── changelog.rst
    │   ├── code_of_conduct.rst
    │   ├── conf.py
    │   ├── index.rst
    │   ├── installation.rst
    │   ├── make.bat
    │   ├── Makefile
    │   ├── readme.rst
    │   ├── requirements.txt
    │   ├── _static
    │   │   └── custom_cookietemple.css
    │   └── usage.rst
    ├── .editorconfig
    ├── exploding_springfield
    │   ├── cli_pytorch.py
    │   ├── cli_tensorflow.py
    │   ├── cli_xgboost.py
    │   ├── data
    │   │   └── xgboost_test_data.tsv
    │   ├── __init__.py
    │   ├── models
    │   │   └── xgboost_test_model.xgb
    ├── .gitattributes
    ├── .github
    │   ├── dependabot.yml
    │   ├── ISSUE_TEMPLATE
    │   │   ├── bug_report.md
    │   │   ├── feature_request.md
    │   │   └── general_question.md
    │   ├── pull_request_template.md
    │   └── workflows
    │       ├── build_docs.yml
    │       ├── build_package.yml
    │       ├── pr_to_master_from_patch_release_only.yml
    │       ├── publish_package.yml
    │       ├── run_bandit.yml
    │       ├── run_flake8_linting.yml
    │       ├── run_mlf_core_lint.yml
    │       └── sync.yml
    ├── .gitignore
    ├── LICENSE
    ├── Makefile
    ├── makefiles
    │   ├── Linux.mk
    │   └── Windows.mk
    ├── MANIFEST.in
    ├── mlf_core.cfg
    ├── .mlf_core.yml
    ├── README.rst
    ├── .readthedocs.yml
    ├── requirements_dev.txt
    ├── requirements.txt
    ├── setup.cfg
    └── setup.py

Included frameworks/libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. `setuptools <https://setuptools.readthedocs.io/en/latest/>`_ for code packaging
2. `click <https://click.palletsprojects.com/>`_ for the command line interface
3. One of `Pytorch <https://pytorch.org/>`_, `Tensorflow <https://www.tensorflow.org/>`_ or `XGBoost <https://xgboost.readthedocs.io/en/latest/>`_,
4. Preconfigured `readthedocs <https://readthedocs.org/>`_
5. Six Github workflows:

  1. ``build_docs.yml``, which builds the readthedocs documentation.
  2. ``build_package.yml``, which builds the cli-python package.
  3. ``run_flake8_linting.yml``, which runs `flake8 <https://flake8.pycqa.org/en/latest/>`_ linting.
  4. ``publish_package.yml``, which publishes the package to PyPi. Note that it only runs on Github release and requires PyPi secrets to be set up.
  5. ``run_bandit``, run `bandit <https://github.com/PyCQA/bandit>`_ to discover security issues in your python code
  6. ``pr_to_master_from_patch_release_only``: Please read :ref:`pr_master_workflow_docs`.

Publishing the package to PyPI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ensure that your package builds and passes any twine checks. The ``build_package.yml`` workflow verifies both.
If the workflow passes you should open a pull request to ``master`` and merge it after reviews.
The only thing left to do now is to create a release on Github.
**Ensure that your PyPI secrets are set.** Follow the instructions on `Encrypted Secrets <https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets>`_ if required.
