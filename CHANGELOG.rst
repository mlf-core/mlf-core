.. _changelog_f:

==========
Changelog
==========

This project adheres to `Semantic Versioning <https://semver.org/>`_.

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
