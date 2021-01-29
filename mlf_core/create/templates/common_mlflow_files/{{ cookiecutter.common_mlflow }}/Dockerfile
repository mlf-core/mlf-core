FROM mlfcore/base:1.1.0

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

# https://pytorch.org/docs/stable/generated/torch.set_deterministic.html#torch.set_deterministic
ENV CUBLAS_WORKSPACE_CONFIG=:16:8
ENV CUBLAS_WORKSPACE_CONFIG=:4096:8
