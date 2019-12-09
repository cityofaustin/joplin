# joplin-base

FROM python:3.7.5-slim-stretch as joplin-base

# jq for sanitizing backup data on hosted container
RUN apt-get update && apt-get install -y gnupg curl jq
# dependencies required for psycopg2
RUN apt-get install -y libpq-dev gcc
RUN pip install pipenv

# PostgreSQL 10
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' >  /etc/apt/sources.list.d/pgdg.list \
    && curl -s https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update && apt-get install -y postgresql-client

# Set Environment Variables
ENV PYTHONUNBUFFERED=1
ENV WEB_CONCURRENCY=3
ENV PORT ${PORT:-80}
EXPOSE $PORT
