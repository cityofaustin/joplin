FROM python:3.6.5-slim-stretch

# GnuPG, Curl
RUN apt-get update && apt-get install -y gnupg curl

# PostgreSQL 10
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' >  /etc/apt/sources.list.d/pgdg.list \
    && curl -s https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update && apt-get install -y postgresql-client

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get update; apt-get -y install nodejs
RUN npm install --global yarn

COPY /deploy/requirements.txt /deploy/requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check --requirement /deploy/requirements.txt

ENV PYTHONUNBUFFERED=1
ENV WEB_CONCURRENCY=4
ENV PORT ${PORT:-80}
EXPOSE $PORT

RUN mkdir /app
WORKDIR /app

COPY "$PWD/joplin" /app/joplin
COPY "$PWD/media" /app/media

WORKDIR /app/joplin
RUN yarn; yarn build
WORKDIR /app

COPY "$PWD/migrate-load-data.sh" /app/migrate-load-data.sh
COPY "$PWD/docker-entrypoint-prod.sh" /app/docker-entrypoint-prod.sh
ENTRYPOINT ["./docker-entrypoint-prod.sh"]

CMD ["gunicorn", "joplin.wsgi:application", "--pythonpath", "/app/joplin"]
