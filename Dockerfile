ARG NVIDIA_CUDA_TAG
# bring in the micromamba image so we can copy files from it
FROM mambaorg/micromamba:0.25.1 as micromamba

# This is the image we are going add micromaba to:
ARG NVIDIA_CUDA_TAG
FROM nvidia/cuda:${NVIDIA_CUDA_TAG} as base

ARG USERNAME
ARG USER_ID
ARG GROUP_ID
ARG PROJECT_PATH

ARG MAMBA_USER=${USERNAME}
ARG MAMBA_USER_ID=${USER_ID}
ARG MAMBA_USER_GID=${GROUP_ID}
ENV MAMBA_USER=$MAMBA_USER
ENV MAMBA_ROOT_PREFIX="/opt/conda"
ENV MAMBA_EXE="/bin/micromamba"

COPY --from=micromamba "$MAMBA_EXE" "$MAMBA_EXE"
COPY --from=micromamba /usr/local/bin/_activate_current_env.sh /usr/local/bin/_activate_current_env.sh
COPY --from=micromamba /usr/local/bin/_dockerfile_shell.sh /usr/local/bin/_dockerfile_shell.sh
COPY --from=micromamba /usr/local/bin/_entrypoint.sh /usr/local/bin/_entrypoint.sh
COPY --from=micromamba /usr/local/bin/_activate_current_env.sh /usr/local/bin/_activate_current_env.sh
COPY --from=micromamba /usr/local/bin/_dockerfile_initialize_user_accounts.sh /usr/local/bin/_dockerfile_initialize_user_accounts.sh
COPY --from=micromamba /usr/local/bin/_dockerfile_setup_root_prefix.sh /usr/local/bin/_dockerfile_setup_root_prefix.sh

RUN /usr/local/bin/_dockerfile_initialize_user_accounts.sh && \
    /usr/local/bin/_dockerfile_setup_root_prefix.sh

USER $MAMBA_USER

SHELL ["/usr/local/bin/_dockerfile_shell.sh"]

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]
# Optional: if you want to customize the ENTRYPOINT and have a conda
# environment activated, then do this:
# ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "my_entrypoint_program"]

# You can modify the CMD statement as needed....
CMD ["/bin/bash"]
WORKDIR ${PROJECT_PATH}

#COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yaml /tmp/environment.yaml

#RUN micromamba install -y -n base -f /tmp/environment.yaml && \
#    micromamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Check https://pytorch.org/get-started/previous-versions/#v171
# to install a PyTorch version suitable for your OS and CUDA
# or feel free to adapt the code to a newer PyTorch version
RUN micromamba create --name kaznerd python=3.8 -c conda-forge && \
    eval "$(micromamba shell hook --shell=bash)" &&\
    micromamba activate kaznerd &&\
    micromamba install -c anaconda numpy &&\
    micromamba install -c conda-forge seqeval &&\
    pip install torch==1.7.1+cu101 torchvision==0.8.2+cu101 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html &&\
    pip install transformers &&\
    pip install datasets &&\
    micromamba clean --all --yes
