FROM python:3.6.5-slim-stretch

# Make Bash our default shell
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# GnuPG, Curl, and OpenSSH, iproute2
RUN apt-get update && apt-get install -y gnupg curl openssh-server iproute2
RUN groupadd -g 33 sshd && useradd -u 33 -g 33 -c sshd -d / sshd

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
EXPOSE $PORT 22

RUN mkdir /app
WORKDIR /app

# .profile.d is necessary for heroku-exec (ps:exec) methods (SSH tunneling)
#  https://devcenter.heroku.com/articles/exec#enabling-docker-support
COPY "$PWD/.profile.d" /app/.profile.d
COPY "$PWD/fixtures" /app/fixtures
COPY "$PWD/joplin" /app/joplin

WORKDIR /app/joplin
RUN yarn; yarn build
WORKDIR /app

COPY "$PWD/migrate-load-data.sh" /app/migrate-load-data.sh
COPY "$PWD/docker-entrypoint-prod.sh" /app/docker-entrypoint-prod.sh
ENTRYPOINT ["./docker-entrypoint-prod.sh"]

#CMD ["gunicorn", "joplin.wsgi:application", "--pythonpath", "/app/joplin"]
CMD bash /app/.profile.d/heroku-exec.sh &&  gunicorn joplin.wsgi:application --pythonpath /app/joplin
