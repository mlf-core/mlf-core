FROM mlfcore/base:1.0.0

# Install the conda environment
COPY environment.yml .
RUN conda env create -f environment.yml && conda clean -a

# Activate the environment
RUN echo "source activate exploding_springfield" >> ~/.bashrc
ENV PATH /home/user/miniconda/envs/exploding_springfield/bin:$PATH

# Dump the details of the installed packages to a file for posterity
RUN conda env export --name exploding_springfield > exploding_springfield_environment.yml

# Currently required, since mlflow writes every file as root!
USER root
