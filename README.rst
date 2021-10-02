.. image:: https://user-images.githubusercontent.com/21954664/84388841-84b4cc80-abf5-11ea-83f3-b8ce8de36e25.png
    :target: https://mlf-core.com
    :alt: mlf-core logo

|

========
mlf-core
========

|PyPI| |Python Version| |License| |Read the Docs| |Build| |Tests| |Codecov| |pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/mlf-core.svg
   :target: https://pypi.org/project/mlf-core/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/mlf-core
   :target: https://pypi.org/project/mlf-core
   :alt: Python Version
.. |License| image:: https://img.shields.io/github/license/mlf-core/mlf-core
   :target: https://opensource.org/licenses/Apache-2.0
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/mlf-core/latest.svg?label=Read%20the%20Docs
   :target: https://mlf-core.readthedocs.io/
   :alt: Read the documentation at https://mlf-core.readthedocs.io/
.. |Build| image:: https://github.com/mlf-core/mlf-core/workflows/Build%20mlf-core%20Package/badge.svg
   :target: https://github.com/mlf-core/mlf-core/actions?workflow=Package
   :alt: Build Package Status
.. |Tests| image:: https://github.com/mlf-core/mlf-core/workflows/Run%20mlf-core%20Tests/badge.svg
   :target: https://github.com/mlf-core/mlf-core/actions?workflow=Tests
   :alt: Run Tests Status
.. |Codecov| image:: https://codecov.io/gh/mlf-core/mlf-core/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/mlf-core/mlf-core
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black
.. image:: https://static.pepy.tech/personalized-badge/mlf-core?units=international_system&left_color=grey&right_color=green&left_text=Downloads
   :target: https://pepy.tech/project/mlf-core
   :alt: Pepy Downloads

.. image:: https://img.shields.io/discord/742367395196305489?color=passing
   :target: https://discord.gg/Mv8sAcq
   :alt: Discord


Overview
--------

.. figure:: https://user-images.githubusercontent.com/31141763/110704981-02921c80-81f6-11eb-8775-bd73f565568c.png
   :alt: mlf-core overview

   mlf-core provides CPU and GPU deterministic machine learning templates based on MLflow, Conda, Docker and a strong Github integration.
   Templates are available for PyTorch, TensorFlow and XGBoost.
   A custom linter ensures that projects stay deterministic in all phases of development and deployment.

Installing
---------------

Start your journey with mlf-core by installing it via ``$ pip install mlf-core``.

See `Installation  <https://mlf_core.readthedocs.io/en/latest/readme.html#installing>`_.

run
----
See a mlf-core project in action.

.. figure:: https://user-images.githubusercontent.com/31141763/117714817-c409e580-b1d7-11eb-9991-cb6eb58efbb7.gif


config
------
Configure mlf-core to get started.

.. figure:: https://user-images.githubusercontent.com/31141763/102669098-f6199d00-418d-11eb-9ae6-26c12d9c1231.gif

See `Configuring mlf-core <https://mlf_core.readthedocs.io/en/latest/config.html>`_

list
----
List all available mlf-core templates.

.. figure:: https://user-images.githubusercontent.com/31141763/102668939-8d322500-418d-11eb-8b2c-acd895fc50e3.gif

See `Listing all templates <https://mlf_core.readthedocs.io/en/latest/list_info.html#list>`_.

info
----
Get detailed information on a mlf-core template.

.. figure:: https://user-images.githubusercontent.com/31141763/102669191-324cfd80-418e-11eb-9542-d2995b7318a9.gif

See `Get detailed template information <https://mlf_core.readthedocs.io/en/latest/list_info.html#info>`_.

create
------
Kickstart your deterministic machine laerning project with one of mlf-core's templates in no time.

.. figure:: https://user-images.githubusercontent.com/31141763/102669143-1184a800-418e-11eb-853b-0deb0387efc6.gif

See `Create a project <https://mlf_core.readthedocs.io/en/latest/create.html>`_.

lint
----
Use advanced linting to ensure your project always adheres to mlf-core's standards and stays deterministic.

.. image:: https://user-images.githubusercontent.com/31141763/102668893-696edf00-418d-11eb-888e-822244a6f5dc.gif

See `Linting your project <https://mlf_core.readthedocs.io/en/latest/lint.html>`_

bump-version
------------
Bump your project version across several files.

.. figure:: https://user-images.githubusercontent.com/31141763/102668987-aaff8a00-418d-11eb-9292-dc512f77f09b.gif

See `Bumping the version of an existing project  <https://mlf_core.readthedocs.io/en/latest/bump_version.html>`_.

sync
------
Sync your project with the latest mlf-core release to get the latest template features.

.. figure:: https://user-images.githubusercontent.com/31141763/102669065-de421900-418d-11eb-9e1b-a76487d02b2a.gif

See `Syncing a project <https://mlf_core.readthedocs.io/en/latest/sync.html>`_.

upgrade
-------
Check whether you are using the latest mlf-core version and update automatically to benefit from the latest features.

See `<https://mlf_core.readthedocs.io/en/latest/upgrade.html>`_.


Credits
-------

Primary idea and main development by `Lukas Heumos <https://github.com/zethson/>`_. mlf-core is inspired by nf-core_.
This package was created with cookietemple_ based on a modified `audreyr/cookiecutter-pypackage`_ project template using cookiecutter_.

.. _MLflow: https://mlflow.org
.. _cookietemple: https://cookietemple.com
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT: http://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern_Python_Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _pip: https://pip.pypa.io/
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://mlf-core.readthedocs.io/en/latest/usage.html
.. _cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _nf-core: https://nf-co.re
