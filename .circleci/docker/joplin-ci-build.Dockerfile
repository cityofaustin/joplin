##########
# add docker 18.09 so we can use BUILDKIT=1
# uses alpine linux as its base
##########
FROM docker:18.09.6

# Install herokucli (requires nodejs to install)
ENV NODE_VERSION 12.3.0
ARG HEROKU_CLI_VERSION='7.6.0'
RUN apk add nodejs
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
RUN yarn global add heroku@$HEROKU_CLI_VERSION

# Install yarn
ENV YARN_VERSION 1.16.0
RUN apk add yarn

# Install aws-cli
ARG AWS_CLI_VERSION='1.16.145'
RUN apk add --update \
  python \
  python-dev \
  py-pip \
  build-base \
  && pip install awscli==$AWSCLI_VERSION \
  && apk --purge -v del py-pip

# bash for running scripts
# git, openssh-client for git (to run "checkout" step in config.yml)
# curl, gnupg for psql
RUN apk add --no-cache \
  bash \
  git openssh-client \
  curl gnupg

# Add psql 10 cli
RUN apk add --update postgresql-client

# Remove build cache
RUN rm -rf /var/cache/apk/*
