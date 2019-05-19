########################################################
# joplin-base

FROM python:3.6.5-slim-stretch as joplin-base

RUN apt-get update && apt-get install -y gnupg curl

# PostgreSQL 10
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' >  /etc/apt/sources.list.d/pgdg.list \
    && curl -s https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update && apt-get install -y postgresql-client

COPY /deploy/requirements.txt /deploy/requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check --requirement /deploy/requirements.txt

ENV PYTHONUNBUFFERED=1
ENV WEB_CONCURRENCY=4
ENV PORT ${PORT:-80}
EXPOSE $PORT

RUN mkdir /app
WORKDIR /app

COPY "$PWD/joplin" /app/joplin
COPY "$PWD/media" /app
COPY "$PWD/docker-entrypoint.sh" /app/docker-entrypoint.sh
COPY "$PWD/migrate-load-data.sh" /app/migrate-load-data.sh

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["gunicorn", "joplin.wsgi:application", "--pythonpath", "/app/joplin"]

########################################################
# joplin-base => joplin-local

FROM joplin-base as joplin-local

ENV ENV "local"

########################################################
# joplin-base => joplin-deployed

FROM joplin-base as joplin-deployed

# Install nodejs dependencies for deployed builds
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get update; apt-get -y install nodejs
RUN npm install --global yarn

WORKDIR /app/joplin
RUN npm rebuild node-sass
RUN yarn; yarn build
WORKDIR /app

########################################################
# joplin-base => joplin-deployed => joplin-dev

FROM joplin-deployed as joplin-dev

ENV ENV "dev"

########################################################
# joplin-base => joplin-deployed => joplin-staging

FROM joplin-base as joplin-staging

ENV ENV "staging"

########################################################
# joplin-base => joplin-deployed => joplin-prod

FROM joplin-base as joplin-prod

ENV ENV "prod"
