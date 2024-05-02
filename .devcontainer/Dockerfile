FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

RUN python3 -m pip install poetry~=1.8.2
RUN ln -s /usr/share/bash-completion/completions/git /usr/share/bash-completion/bash_completion

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y sshpass
RUN apt-get clean

WORKDIR /workspaces/ansible


COPY poetry.lock pyproject.toml .
RUN chown -R vscode:vscode /workspaces

USER vscode
# make prompt multiline cause it's too long by default
RUN sed -i -E -e '/PS1="\$/c\    PS1="${userpart} ${lightblue}\\w ${gitbranch}${removecolor}\\n\\$ "' ~/.bashrc

RUN poetry install
RUN VN=$(poetry env list | head -n 1 | cut -d ' ' -f 1) && ln -s ~/.cache/pypoetry/virtualenvs/$VN ~/venv
