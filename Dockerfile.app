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

########################################################
# test
FROM joplin-base as joplin-test-test-test
ENV IS_TEST_TEST_TEST "this should not be included in any builds"

########################################################
# joplin-base => joplin-local

FROM joplin-base as joplin-local

COPY "$PWD/joplin" /app/joplin
COPY "$PWD/media" /app
COPY "$PWD/docker-entrypoint.sh" /app/docker-entrypoint.sh
COPY "$PWD/migrate-load-data.sh" /app/migrate-load-data.sh

# for testing only
ENV IS_LOCAL "true"

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["gunicorn", "joplin.wsgi:application", "--pythonpath", "/app/joplin"]

########################################################
# joplin-base => joplin-local => joplin-migration-test

FROM joplin-base as joplin-migration-test

# TODO: clone form github

# for testing only
ENV IS_MIGRATION_TEST "true"

########################################################
# joplin-base => joplin-local => joplin-heroku

FROM joplin-local as joplin-heroku

# TODO
# need to run yarn build?
# use different entrypoint?
# Why is there an entrypoint-prod yet the normal entrypoint has logic to handle production things?

########################################################
# joplin-base => joplin-local => joplin-production

FROM joplin-local as joplin-production

# TODO
# Maybe no difference between heroku/production Dockerfiles?
