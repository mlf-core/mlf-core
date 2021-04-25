FROM mlfcore/base:1.2.0

# Install the conda environment
COPY environment.yml .
RUN conda env create -f environment.yml && conda clean -a

# Activate the environment
RUN echo "source activate {{ cookiecutter.project_slug_no_hyphen }}" >> ~/.bashrc
ENV PATH /home/user/miniconda/envs/{{ cookiecutter.project_slug_no_hyphen }}/bin:$PATH

# Dump the details of the installed packages to a file for posterity
RUN conda env export --name {{ cookiecutter.project_slug }} > {{ cookiecutter.project_slug }}_environment.yml

# Currently required, since mlflow writes every file as root!
USER root

# Tensorflow has issues finding libcudnn8 from the base NVIDIA Container so we reinstall it
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcudnn8_8.1.1.33-1+cuda11.2_amd64.deb
RUN apt install ./libcudnn8_8.1.1.33-1+cuda11.2_amd64.deb
