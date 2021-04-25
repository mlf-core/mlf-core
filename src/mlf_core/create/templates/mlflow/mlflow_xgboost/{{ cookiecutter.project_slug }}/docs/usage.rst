Usage
=============

Setup
-------

mlf-core based mlflow projects require either Conda or Docker to be installed.
The usage of Docker is highly preferred, since it ensures that system-intelligence can fetch all required and accessible hardware.
This cannot be guaranteed for Mac let alone Windows environments.

Conda
+++++++

There is no further setup required besides having Conda installed and CUDA configured for GPU support.
mlflow will create a new environment for every run.

Docker
++++++++

If you use Docker you should not need to build the Docker container manually, since it should be available on Github Packages or another registry.
However, if you want to build it manually for e.g. development purposes, ensure that the names matches the defined name in the ``MLproject``file.
This is sufficient to train on the CPU. If you want to train using the GPU you need to have the `NVIDIA Container Toolkit <https://github.com/NVIDIA/nvidia-docker>`_ installed.

Training
-----------

Training on the CPU
+++++++++++++++++++++++

Set your desired environment in the MLproject file. Start training using ``mlflow run .``.
You need to disable CUDA to train on the CPU! See :ref:`parameters`.

Training using GPUs
+++++++++++++++++++++++

Conda environments will automatically use the GPU if available.
Docker requires the accessible GPUs to be passed as runtime parameters. To train using all gpus run ``mlflow run . -A gpus=all``.
You can replace ``all`` with specific GPU ids (e.g. 0) if desired.

Parameters
+++++++++++++++

- cuda:                       Whether to train with CUDA support (=GPU)                   ['True': string]
- max_epochs:                 Number of epochs to train                                   [25:        int]
- general-seed:               Python, Random, Numpy seed                                  [0:         int]
- xgboost-seed:               XGBoost specific seed                                       [0:         int]
- single-precision-histogram  Whether to enable `single precision for histogram building <https://xgboost.readthedocs.io/en/latest/parameter.html#additional-parameters-for-hist-and-gpu-hist-tree-method>`_ ['True': string]

TODO MLF-CORE: Write your usage and parameter documentation here.
