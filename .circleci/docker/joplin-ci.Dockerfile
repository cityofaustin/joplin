##########
# add docker 18.09 so we can use BUILDKIT=1
# uses alpine linux as its base
##########
FROM docker:18.09.6

# bash for running scripts
# git, openssh-client for git (to run "checkout" step in config.yml)
# curl, gnupg for psql
RUN apk add --no-cache \
  bash \
  git openssh-client \
  curl gnupg

# Install herokucli (requires nodejs to install)
RUN curl https://cli-assets.heroku.com/install.sh | sh

# Install aws-cli
ARG AWS_CLI_VERSION='1.16.145'
RUN apk add --update \
  python \
  python-dev \
  py-pip \
  build-base \
  && pip install awscli==$AWSCLI_VERSION \
  && apk --purge -v del py-pip

# Add psql 10 cli
RUN apk add --update postgresql-client

# Remove build cache
RUN rm -rf /var/cache/apk/*
