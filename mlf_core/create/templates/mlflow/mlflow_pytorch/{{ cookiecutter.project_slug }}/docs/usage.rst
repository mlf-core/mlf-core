Usage
=============

Setup
-------

mlf-core based mlflow projects require either Conda or Docker to be installed.
The usage of Docker is highly preferred, since it ensures that system-intelligence can fetch all required and accessible hardware.
This cannot be guaranteed for MacOS let alone Windows environments.

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
No further parameters are required.

Training using GPUs
+++++++++++++++++++++++

Conda environments will automatically use the GPU if available.
Docker requires the accessible GPUs to be passed as runtime parameters. To train using all gpus run ``mlflow run . -A t-A gpus=all -P gpus=<<num_of_gpus>> -P acc=ddp``.
To train only on CPU it is sufficient to call ``mlflow run . -A t``. To train on a single GPU, you can call ``mlflow run . -A t -A gpus=all -P gpus=1`` and for multiple GPUs (for example 2)
``mlflow run . -A t -A gpus=all -P gpus=2 -P accelerator=ddp``.
You can replace ``all`` with specific GPU ids (e.g. 0) if desired.

Parameters
+++++++++++++++

- gpus                        Number of gpus to train with                             [0:         int]
- accelerator                 Accelerator connecting to the Lightning Trainer          ['None'  string]
- max_epochs:                 Number of epochs to train                                [5:         int]
- general-seed:               Python, Random, Numpy seed                               [0:         int]
- pytorch-seed:               Pytorch specific seed                                    [0:         int]
- training-batch-size:        Batch size for training batches                          [64:        int]
- test-batch-size:            Batch size for test batches                              [1000:      int]
- lr:                         Learning rate of the optimizer                           [0.01:    float]
- log-interval:               Number of batches to train for before logging            [100:       int]

TODO MLF-CORE: Write your usage and parameter documentation here.
