##########
# add python so we can install using pip
# uses debian linux as its base
##########
FROM python:3.6.5-slim-stretch

# apt-utils for installs
# bash for scripts
# curl, gnupg for psql
# git, openssh-client for git
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
  apt-utils \
  bash \
  curl gnupg \
  git openssh-client

# Add psql 10 CLI
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' >  /etc/apt/sources.list.d/pgdg.list \
    && curl -s https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update && apt-get install -y postgresql-client

# Add Heroku CLI
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Add AWS CLI
ARG AWS_CLI_VERSION='1.16.145'
RUN pip install --no-cache-dir awscli==$AWS_CLI_VERSION
