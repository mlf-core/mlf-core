mlflow-xgboost
-------------------

Purpose
^^^^^^^^

mlflow-xgboost is a `MLflow <https://mlflow.org/>`_ based template designed for `XGBoost <https://xgboost.readthedocs.io>`_ machine learning models.
The project is fully CPU and GPU deterministic with `system-intelligence <https://github.com/mlf-core/system-intelligence>`_ integration.
Additionally, Conda and Docker are supported out of the box.

Design
^^^^^^^^

The package follows the mlf-core convention of a single environment.yml file in conjunction with an mlf-core based Dockerfile.
As required a MLproject file serves as entry point and parameter definition.

.. code::

    ├── AUTHORS.rst
    ├── .bandit.yml
    ├── CHANGELOG.rst
    ├── CODE_OF_CONDUCT.rst
    ├── Dockerfile
    ├── docs
    │   ├── authors.rst
    │   ├── changelog.rst
    │   ├── code_of_conduct.rst
    │   ├── conf.py
    │   ├── index.rst
    │   ├── make.bat
    │   ├── Makefile
    │   ├── model.rst
    │   ├── readme.rst
    │   ├── requirements.txt
    │   ├── _static
    │   │   └── custom_cookietemple.css
    │   └── usage.rst
    ├── .editorconfig
    ├── environment.yml
    ├── exploding_springfield
    │   ├── data_loading
    │   │   ├── data_loader.py
    │   ├── exploding_springfield.py
    │   ├── mlf_core
    │   │   ├── mlf_core.py
    ├── .flake8
    ├── .github
    │   ├── ISSUE_TEMPLATE
    │   │   ├── bug_report.md
    │   │   ├── feature_request.md
    │   │   ├── general_question.md
    │   │   └── sync_notify.md
    │   ├── pull_request_template.md
    │   └── workflows
    │       ├── build_docs.yml
    │       ├── mlf_core_lint.yml
    │       ├── pr_to_master_from_patch_release_only.yml
    │       ├── run_bandit.yml
    │       ├── run_flake8_linting.yml
    │       ├── sync.yml
    │       └── train_cpu.yml
    ├── .gitignore
    ├── LICENSE
    ├── mlf_core.cfg
    ├── .mlf_core.yml
    ├── MLproject
    ├── README.rst
    └── .readthedocs.yml
    
Included frameworks/libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. `MLflow <https://mlflow.org/>`_ as the primary framework for parameter and artifact logging.
2. `XGBoost <https://xgboost.readthedocs.io>`_ as the primary machine learning library.
3. `system-intelligence <https://github.com/mlf-core/system-intelligence>`_ to fetch all hardware related information.
4. Preconfigured `readthedocs <https://readthedocs.org/>`_
5. Five Github workflows:

  1. ``build_docs.yml``, which builds the readthedocs documentation.
  2. ``run_flake8_linting.yml``, which runs `flake8 <https://flake8.pycqa.org/en/latest/>`_ linting.
  3. ``pr_to_master_from_patch_release_only.yml`` Please read :ref:`pr_master_workflow_docs`.
  4. ``train_cpu.yml``, which trains the model on the CPU for a small number of epochs. Requires the data to be accessible.
  5. ``sync.yml``, which checks whether a new version of mlflow-pytorch is available and submits a pull request if so.
  6. ``run_mlf_core_lint.yml``, which runs ``mlf-core lint`` to verify that the project adheres to all mlf-core standards.
  7. ``run_bandit.yml``, which runs `Bandit <https://pypi.org/project/bandit/>`_ to find any security issues.


.. include:: mlflow_shared_usage_faq.rst
