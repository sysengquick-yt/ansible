FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# OCI labels
LABEL org.opencontainers.image.source="https://github.com/sysengquick-yt/ansible"
LABEL org.opencontainers.image.description="Devcontainer for sysengquick 2024 tutorial"
LABEL org.opencontainers.image.licenses="GPL-3.0"

# install poetry for python dependencies
RUN python3 -m pip install poetry~=1.8.2

# enable bash completion for git
RUN ln -s /usr/share/bash-completion/completions/git /usr/share/bash-completion/bash_completion

# install useful system packages
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y sshpass vim iputils-ping
RUN apt-get clean

# install vault cli
ARG VAULT_VERSION=1.16.2
RUN curl -Lo /tmp/vault.zip \
    https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip \
    && cd /usr/local/bin \
    && unzip /tmp/vault.zip \
    && rm -f /tmp/vault.zip

# setup non-root user
USER vscode
WORKDIR /workspaces/ansible

# make prompt multiline cause it's too long by default
RUN sed -i -E -e '/PS1="\$/c\    PS1=" ${userpart} ${lightblue}\\w ${gitbranch}${removecolor}\\n\\$ "' ~/.bashrc
RUN echo 'export VAULT_ADDR="https://vault.local.technoplaza.net:8200"' >> ~/.bashrc
RUN echo 'export VAULT_SKIP_VERIFY=1' >> ~/.bashrc

# install poetry venv and symlink to ~/venv
COPY poetry.lock pyproject.toml .
RUN poetry install
RUN VN=$(poetry env list | head -n 1 | cut -d ' ' -f 1) && ln -s ~/.cache/pypoetry/virtualenvs/$VN ~/venv

# install collection (to get dependencies)
ENV COLLECTION=collections/ansible_collections/sysengquick/tutorial
COPY $COLLECTION/galaxy.yml .
RUN poetry run -- ansible-galaxy collection install .

# remove empty collection directory so it finds the one in our git repo
RUN rm -rf ~/.ansible/$COLLECTION
