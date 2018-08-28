FROM python:3.6.5-slim-stretch

RUN apt-get update; apt-get -y install gnupg; apt-get -y install curl
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get update; apt-get -y install nodejs
RUN npm install --global yarn

COPY /deploy/requirements.txt /deploy/requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check --requirement /deploy/requirements.txt

ENV PYTHONUNBUFFERED=1
ENV WEB_CONCURRENCY=4
ENV DEPLOYMENT_MODE="STAGING"
ENV PORT ${PORT:-80}
EXPOSE $PORT

RUN mkdir /app
WORKDIR /app

COPY "$PWD/fixtures" /app/fixtures
COPY "$PWD/joplin" /app/joplin

COPY "$PWD/migrate-load-data.sh" /app/migrate-load-data.sh
#RUN LOAD_DATA=on ./migrate-load-data.sh

WORKDIR /app/joplin
RUN yarn; yarn build
WORKDIR /app

CMD ["gunicorn", "joplin.wsgi:application", "--pythonpath", "/app/joplin"]
