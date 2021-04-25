Usage
^^^^^^^^
It is strongly advised to use Docker to run mlf-core models, since support for other OS besides Linux is limited and dependency management is greatly simplified.

Building the Docker container
+++++++++++++++++++++++++++++++++

The name (=tag) of the Docker Container is specified in the MLproject file in ``image:``.
If you created your project with mlf-core's Github support your Docker container should automatically be building in your Github Container Registry.
Furthermore, it should match the name specified in the MLproject file.
If the Docker container is not available in your Github Container Registry for any reason you must build it locally.
Run: ``docker build -t ghcr.io/GITHUB_USERNAME/PROJECT_SLUG:version .``, where ``PROJECT_SLUG`` is your project's name and ``version`` the current project version.
The MLproject file can always be examined to determine the required Docker container tag.

Running the project with Docker
+++++++++++++++++++++++++++++++++

After having build the Docker container you can now launch your project with ``mlflow run .``.
The Docker container will automatically spin up.

**Note** if you want to run your project with GPU support you must have the `NVIDIA Container Toolkit <https://github.com/NVIDIA/nvidia-docker>`_ installed.
Moreover, you need to pass additional Docker runtime arguments e.g. ``mlflow run . -A gpus=all``, which makes all available GPUs accessible to the Docker container.

Running the project with Conda
+++++++++++++++++++++++++++++++++

Running the project using Conda is possible, but discouraged, since `system-intelligence <https://github.com/mlf-core/system-intelligence>`_ currently only really supports Linux.
Comment out ``docker_env`` and comment in ``conda_env``. Now run the project using e.g. ``mlflow run .``.
GPUs will be automatically be detected and used.

FAQ
^^^^^^

I am using Docker but no GPUs are used for training!
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Please ensure that you have CUDA configured, the `NVIDIA Container Toolkit <https://github.com/NVIDIA/nvidia-docker>`_ installed and pass ``-A gpus=all`` when running the project.
