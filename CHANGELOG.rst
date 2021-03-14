.. _changelog_f:

==========
Changelog
==========

This project adheres to `Semantic Versioning <https://semver.org/>`_.

1.10.0 (2021-03-11)
-------------------

**Added**

* Tutorial accessible at: mlf-core.com/tutorial (#159)
* [ALL TEMPLATES] Removed AUTHORS.rst and moved content into docs/authors.rst (#267)
* [ALL TEMPLATES] Added boto3 to environment to allow for S3 accessibility (#278)
* [ALL TEMPLATES] Workflows, that were triggered when pusing/pr to default master branch do now accept main as default branch

**Fixed**

* Bandit complaining about insecure md5
* mlf-core pytorch template creation and updated its dependencies versions accordingly (#298)
* Pytorch template hparam logging with tensorboard now working
* blacklisted files for sync defined by the user are now correctly picked up
* blacklisted sync files, that are newly introduced by a PR are now included in the sync PR, they were introduced but not in the following ones

**Dependencies**

**Deprecated**


1.9.1 (2021-02-16)
------------------

**Added**

**Fixed**

* [ALL TEMPLATES] lint badge in README.rst

**Dependencies**

**Deprecated**


1.9.0 (2021-02-16)
------------------

**Added**

* Possibility to log input files in all template with the MLFCore object.
* [ALL TEMPLATES] Using new mlf-core/base:1.2.0 container, which is based on CUDA 11.2.1 and cudnn 8.1
* [PYTORCH] Upgraded Pytorch to 1.7.1
* [PYTORCH] Added set_deterministic
* [ALL TEMPLATES] Using new mlflow autolog
* [ALL TEMPLATES] Changed mlflow autolog for loss to every 1 iteration

**Fixed**

* mlf-core fix-artifact-paths does now operate as expected.
* [ALL TEMPLATES] fixed a path error that causes the general template linter to fail searching for
  subprocess.call([\'conda\', \'env\', \'export\', \'--name\', \'<<project_name>>\'], stdout=conda_env_filehandler) and
  mlflow.log_artifact(f\'{{reports_output_dir}}/<<project_name>>_conda_environment.yml\', artifact_path=\'reports\') in the project's mlf_core.py file

**Dependencies**

**Deprecated**


1.8.0 (2021-02-01)
------------------

**Added**

* fixed sync command: blacklisted files now fully working
* updated sync code to the latest version and added logging
* added a output-directory parameter option to create command, allowing users to specifify the
  directory, where the project should be created
* added a user information before the user is prompted to create a GitHub repo with mlf-core
* added flake8 linting for each create template workflow
* GitHub workflow badges in README now link to the corresponding workflow
* [ALL TEMPLATES] added vscode files to .gitignore for templates
* [ALL TEMPLATES] now feature a mlf-core lint workflow with colored linting result output
* [ALL TEMPLATES] renamed train_cpu workflows to use project_slug (was project_slug_no_hyphen)
* [MLFLOW TEMPLATES] refactored the common files for all mlflow templates into a common files directory
* config default values are now preconfigured values (if any)
* added logging to all commands mlf-core offers
* refactored sync, bump-version and create code (added type hints, fixed some variable scoping)
* [ALL TEMPLATES] replaced click with argparse
* [ALL TEMPLATES] renamed some parameters to harmonize between templates
* [PyTorch Template] New template with autologging via pytorch-lightning and mlflow 1.13.1

**Fixed**

* fixed publish_docs WF for all templates working on main or master branch

* fixed gh_pages setup for default branch main

* fixed a bug causing the check upgrade version function to fail if local version is a SNAPSHOT version

**Dependencies**

**Deprecated**


1.7.8 (2020-12-04)
------------------

**Added**

* Instructions to make Docker container public

**Fixed**

**Dependencies**

**Deprecated**


1.7.7 (2020-11-29)
------------------

**Added**

* Support for deploying the documentation on Github Pages. By default the Documentation is pushed to the gh-pages branch.
  Simply enable Github pages (repository settings) with the gh-pages branch and your documentation will build on ``https://username.github.io/repositoryname``

**Fixed**

* Workflows are now also triggered on PR

**Dependencies**

**Deprecated**


1.7.6 (2020-11-22)
------------------

**Added**

**Fixed**

* Github project creation support due to Github's new main branch

**Dependencies**

**Deprecated**

1.7.5 (2020-11-18)
------------------

**Added**

**Fixed**

sync workflow set-env

**Dependencies**

**Deprecated**


1.7.4 (2020-11-11)
------------------

**Added**

**Fixed**

* Sync now compares against the development branch and not the master branch.

**Dependencies**

**Deprecated**


1.7.3 (2020-11-09)
------------------

**Added**

**Fixed**

* Added CHANGELOG.rst to blacklisted files

**Dependencies**

**Deprecated**


1.7.2 (2020-11-07)
------------------

**Added**

**Fixed**

* Removed redundant print in xgboost

**Dependencies**

**Deprecated**


1.7.1 (2020-11-07)
------------------

**Added**

**Fixed**

* mlf-core sync does now correctly find attributes

**Dependencies**

**Deprecated**


1.7.0 (2020-11-06)
------------------

**Added**

* fix-artifact-paths which replaces the artifact paths with the paths of the current system
* More structured documentation

**Fixed**

* Now using GPUs by default only when GPUs are available for XGBoost templates

**Dependencies**

**Deprecated**


1.6.1 (2020-11-06)
------------------

**Added**

* Workflows for package-prediction
* Documentation for package-prediction

**Fixed**

**Dependencies**

**Deprecated**


1.6.0 (2020-11-02)
------------------

**Added**

* New package templates (package-prediction) for Pytorch, Tensorflow and XGBoost

**Fixed**

**Dependencies**

**Deprecated**


1.5.0 (2020-10-29)
------------------

**Added**

* Check for non-deterministic functions for mlflow-tensorflow linter
* Check for all_reduce for mlflow-xgboost templates
* Check for OS for system-intelligence runs. If not Linux -> don't run system-intelligence
* .gitattributes to templates, which ignores mlruns
* Documentation on creating releases

**Fixed**

* Sync now operates correctly with the correct PR URL

**Dependencies**

**Deprecated**


1.4.4 (2020-10-22)
------------------

**Added**

**Fixed**

* Conda report generation

**Dependencies**

**Deprecated**


1.4.3 (2020-09-17)
------------------

**Added**

**Fixed**

* Internal Github workflows
* Docker documentation

**Dependencies**

**Deprecated**

1.4.2 (2020-09-11)
------------------

**Added**

**Fixed**

* Accidentally left a - in the train_cpu.yml of mlflow-pytorch
* mlflow-pytorch and mlflow-tensorflow now only train for 2 epochs on train_cpu.yml

**Dependencies**

**Deprecated**


1.4.1 (2020-09-10)
------------------

**Added**

**Fixed**

* Github username must now always be lowercase, since Docker does not like uppercase letters
* Fixed train_cpu workflows to use the correct containers

**Dependencies**

**Deprecated**

1.4.0 (2020-08-28)
------------------

**Added**

* model.rst documentation for all templates
* added support for verbose output

**Fixed**

* Publish Docker workflows now use the new Github registry
* Default Docker container names are now   ```image: ghcr.io/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug_no_hyphen }}:{{ cookiecutter.version }}```

**Dependencies**

**Deprecated**


1.3.0 (2020-08-27)
------------------

**Added**

* automatically mounting /data now in all mlflow templates (#56)
* mlflow-xgboost xgboost from 1.1.1 to 1.2.0

**Fixed**

* mlf_core.py now uses project_slug; adapted linter accordingly (#55)
* Removed dask-cuda from mlflow-xgboost

**Dependencies**

**Deprecated**


1.2.2 (2020-08-21)
------------------

**Added**

**Fixed**

* A couple of parameters were not with hyphen -> now default behavior

**Dependencies**

**Deprecated**


1.2.1 (2020-08-21)
------------------

**Added**

**Fixed**

* flake8 for mlflow-pytorch

**Dependencies**

**Deprecated**


1.2.0 (2020-08-21)
------------------

**Added**

* Option --view to config to view the current configuration
* Option --set_token to sync to set the sync token again

**Fixed**

* #41 https://github.com/mlf-core/mlf-core/issues/41 -> mlflow-pytorch multi GPU Support

**Dependencies**

**Deprecated**


1.1.0 (2020-08-19)
------------------

**Added**

* Publish Docker workflow. Publishes to Github Packages per default, but can be configured.
* Linting function, which checks mlflow-pytorch for any used atomic_add functions.
* system-intelligence 1.2.2 -> 1.2.3
* Support for both, MLF-CORE TODO: and TODO MLF-CORE: statements

**Fixed**

* Default project version from 0.1.0 to 0.1.0-SNAPSHOT.
* Outdated screenshots
* Nightly versions now warn instead of wrongly complaining about outdated versions.
* Sync actor, but not yet completely for organizations
* A LOT of documentation
* Now using project_slug_no_hyphen to facilitate the creation of repositories with - characters.
* Removed boston dataset from XGBoost and XGBoost_dask
* Renamed all parameters to use hyphens instead of underscores

**Dependencies**

**Deprecated**


1.0.1 (2020-08-11)
------------------

**Added**

**Fixed**

* Sync workflow now uses the correct secret

**Dependencies**

**Deprecated**


1.0.0 (2020-08-11)
------------------

**Added**

* Created the project using cookietemple
* Added all major commands: create, list, info, lint, sync, bump-version, config, upgrade
* Added mlflow-pytorch, mlflow-tensorflow, mlflow-xgboost, mlflow-xgboost_dask templates

**Fixed**

**Dependencies**

**Deprecated**
