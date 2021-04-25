.. _lint:

=====================
Linting your project
=====================

`Linting <https://en.wikipedia.org/wiki/Lint_(software)>`_ is the process of statically analyzing code to find code style violations and to detect errors.
mlf-core implements a custom linting system, but depending on the template external tools linting tools may additionally be called.

Usage
-----------------------

mlf-core lint can be invoked on an existing project using

.. code-block:: console

    $ mlf-core lint <OPTIONS> <PATH>

mlf-core's linting is divided into three distinct phases.

1. All linting functions, which all templates share are called and the results are collected.
2. Template specific linting functions are invoked and the results are appended to the results of phase 1
3. Template specific external linters are called (e.g. autopep8 for Python based projects)

The linting results of the first two phases are assigned into 3 groups:

.. raw:: html

    <style> .green {color:#008000; } </style>
    <style> .yellow {color:#ffff00; } </style>
    <style> .red {color:#aa0060; } </style>

.. role:: green
.. role:: yellow
.. role:: red

1. :green:`Passed`
2. :yellow:`Passed with warning`
3. :red:`Failed`

If any of the checks failed linting stops and returns an error code.

.. figure:: images/linting_example.png
   :scale: 100 %
   :alt: Linting example

   Linting applied to a newly created mlflow-pytorch project.

To examine the reason for a failed linting test please follow the URL. All reasons are explained in the section :ref:`linting_codes`.

.. _linting_codes:

Linting codes
-----------------

The following error or warning numbers correspond to errors found during linting.
If you are not sure why a specific linting error has occurred you may find more information using the respective error code.

General
^^^^^^^^^

general-1
~~~~~~~~~~

| File not found. This error occurs when your project does not include all of mlf-core's files, which all templates share.
| Please create the file and populate it with appropriate values. You should also critically reflect why it is missing, since
  at the time of the project creation using mlf-core this file should not have been missing!

general-2
~~~~~~~~~

| Dockerfile invalid. This error usually originates from empty Dockerfiles or missing FROM statements.

general-3
~~~~~~~~~

| TODO String found. The origin of this warning are ``mlf-core TODO:`` ``TODO mlf-core:`` or strings in the respective files. Usually, they point to things that should be
  manually configured or require other attention. You may remove them if there is no task for you to be solved.

general-4
~~~~~~~~~

| Cookiecutter string found. This error occurs if something went wrong at the project creation stage. After a project has been created using mlf-core
  there should not be any jinja2 syntax left.

general-5
~~~~~~~~~~

| Versions not consistent. If the version of all files specified in the [bumpversion] sections defined in the qube.cfg file are not consistent,
  this error may be found. Please ensure that the version is consistent! If you need to exclude specific lines from this check please consult :ref:`bump-version`.
  To prevent this error you should only increase the version of your project using :code:`mlf-core bump-version`.

general-6
~~~~~~~~~~~~~

| ``changelog.rst`` invalid. The ``changelog.rst`` file requires that every changelog section has a header with the version and the corresponding release date.
  The version above another changelog section should always be *greater* than the section below (e.g. 1.1.0 above 1.0.0).
  Every section must have the headings ``**Added**``, ``**Fixed**``, ``**Dependencies**`` and ``**Deprecated**``.

mlflow-pytorch
^^^^^^^^^^^^^^^^

mlflow-pytorch-1
~~~~~~~~~~~~~~~~~~

| File not found. This error occurs when your project does not include all of mlflow-pytorch's expected files.
| Please create the file and populate it with appropriate values. You should also critically reflect why it is missing, since
  at the time of the project creation using mlf-core this file should not have been missing!

mlflow-pytorch-2
~~~~~~~~~~~~~~~~~~

| Expected line not found. This error occurs when CPU/GPU deterministic training may no longer be guaranteed, since a required setting has been disabled or removed.
| Currently, mlflow-pytorch expects the following lines in the main entry script:

.. code-block::
    :linenos:

     trainer.deterministic = True,
     trainer.benchmark = False,
     set_general_random_seeds(general_seed),
     set_pytorch_random_seeds(pytorch_seed, num_of_gpus)

| Line 1 enables deterministic training operations
| Line 2 disables the search for the optimal algorithm for specific operations, which may not necessarily be deterministic.
| Line 3 sets the general random seeds (python random, numpy random and python general)
| Line 4 sets the seed of Pytorch

mlflow-pytorch-3
~~~~~~~~~~~~~~~~~~~

| Function operates non-deterministically.
| Several functions and algorithms available in Pytorch are still based on atomic add or other non-deterministic operators. Hence, these functions are not allowed to be used.
| Source: https://pytorch.org/docs/stable/notes/randomness.html
| Currently mlflow-pytorch reports:

.. code-block::
    :linenos:

    'index_add',
    'scatter_add',
    'bincount',
    'embedding_bag',
    'ctc_loss',
    'interpolate',
    'repeat_interleave',
    'index_select'


mlflow-tensorflow
^^^^^^^^^^^^^^^^^^^^^

mlflow-tensorflow-1
~~~~~~~~~~~~~~~~~~~~~~~

| File not found. This error occurs when your project does not include all of mlflow-tensorflow's expected files.
| Please create the file and populate it with appropriate values. You should also critically reflect why it is missing, since
  at the time of the project creation using mlf-core this file should not have been missing!

mlflow-tensorflow-2
~~~~~~~~~~~~~~~~~~~~~~~~~

| Expected line not found. This error occurs when CPU/GPU deterministic training may no longer be guaranteed, since a required setting has been disabled or removed.
| Currently, mlflow-tensorflow expects:

.. code-block::
    :linenos:

    set_general_random_seeds(dict_args["general_seed"]),
    set_tensorflow_random_seeds(dict_args["tensorflow_seed"])
    def set_tensorflow_random_seeds(seed):
        tf.random.set_seed(seed)
        tf.config.threading.set_intra_op_parallelism_threads = 1  # CPU only
        tf.config.threading.set_inter_op_parallelism_threads = 1  # CPU only
        os.environ['TF_DETERMINISTIC_OPS'] = '1'

| Line 1 sets the general random seeds (python random, numpy random and python general)
| Line 2 sets the seed of Tensorflow
| Line 4 fixes the seed of Tensorflow
| Line 5 sets the number of threads within an individual operation for parallelism to 1
| Line 6 sets the number of threads between independent operations for parallelism to 1
| Line 7 enables and forces all deterministic operations

mlflow-tensorflow-3
~~~~~~~~~~~~~~~~~~~~

| Function operates non-deterministically.
| There are a couple of functions left in Tensorflow, which are known to be operating non-deterministically. They are not allowed to be used.

.. code-block::
    :linenos:

    'softmax_cross_entropy_with_logits',
    'sparse_softmax_cross_entropy_with_logits'

mlflow-xgboost
^^^^^^^^^^^^^^^^^

mlflow-xgboost-1
~~~~~~~~~~~~~~~~~~~~~~

| File not found. This error occurs when your project does not include all of mlflow-dask's expected files.
| Please create the file and populate it with appropriate values. You should also critically reflect why it is missing, since
  at the time of the project creation using mlf-core this file should not have been missing!

mlflow-xgboost-2
~~~~~~~~~~~~~~~~~~

| Expected line not found. This error occurs when CPU/GPU deterministic training may no longer be guaranteed, since a required setting has been disabled or removed.
| Currently, mlflow-xgboost expects:

.. code-block::
    :linenos:

    set_general_random_seeds(dict_args["general_seed"]),
    set_xgboost_random_seeds(dict_args["xgboost_seed"], param)
    def set_xgboost_random_seeds(seed, param):
        param['seed'] = seed

| Line 1 sets the general random seeds (python random, numpy random and python general)
| Line 2 sets the seed of XGBoost
| Line 4 fixes the seed of XGBoost

mlflow-xgboost-3
~~~~~~~~~~~~~~~~~~

| The version of XGBoost has to be at least 1.1.0, since this is first version which includes all deterministic operations.
| Refrain from using versions older than 1.1.0, especially when making use of GPUs.

mlflow-xgboost-4
~~~~~~~~~~~~~~~~~~~

| The ``all_reduce`` algorithm in XGBoost may not operate deterministically.
| Source: https://github.com/dmlc/xgboost/issues/5023

mlflow-xgboost_dask
^^^^^^^^^^^^^^^^^^^^^^^^^^

mlflow-xgboost_dask-1
~~~~~~~~~~~~~~~~~~~~~~~~~~~

| File not found. This error occurs when your project does not include all of mlflow-xgboost_dask's expected files.
| Please create the file and populate it with appropriate values. You should also critically reflect why it is missing, since
  at the time of the project creation using mlf-core this file should not have been missing!

mlflow-xgboost_dask-2
~~~~~~~~~~~~~~~~~~~~~~~~~

| Expected line not found. This error occurs when CPU/GPU deterministic training may no longer be guaranteed, since a required setting has been disabled or removed.
| Currently, mlflow-xgboost_dask expects:

.. code-block::
    :linenos:
    
    set_general_random_seeds(dict_args["general_seed"]),
    set_xgboost_dask_random_seeds(dict_args["xgboost_seed"], param)
    def set_xgboost_random_seeds(seed, param):
        param['seed'] = seed

| Line 1 sets the general random seeds (python random, numpy random and python general)
| Line 2 sets the seed of XGBoost
| Line 4 fixes the seed of XGBoost

mlflow-xgboost_dask-3
~~~~~~~~~~~~~~~~~~~~~~~~

| The version of XGBoost has to be at least 1.1.0, since this is first version which includes all deterministic operations.
| Refrain from using versions older than 1.1.0, especially when making use of GPUs.

mlflow-xgboost-4
~~~~~~~~~~~~~~~~~~~

| The ``all_reduce`` algorithm in XGBoost may not operate deterministically.
| Source: https://github.com/dmlc/xgboost/issues/5023
