FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

RUN python3 -m pip install poetry~=1.8.2
RUN ln -s /usr/share/bash-completion/completions/git /usr/share/bash-completion/bash_completion

WORKDIR /workspaces/ansible

COPY poetry.lock pyproject.toml .
RUN chown -R vscode:vscode /workspaces

USER vscode
RUN poetry install
RUN VN=$(poetry env list | head -n 1 | cut -d ' ' -f 1) && ln -s ~/.cache/pypoetry/virtualenvs/$VN ~/venv
