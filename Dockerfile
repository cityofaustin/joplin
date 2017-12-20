FROM python:3.6.3-slim-stretch

RUN mkdir /app /deploy

WORKDIR /app

COPY /deploy/requirements.txt /deploy/requirements.txt

RUN pip install --no-cache-dir -r /deploy/requirements.txt

# TODO: Don't copy fixtures
COPY "$PWD/fixtures" /app/fixtures

COPY "$PWD/docker-entrypoint.sh" /app/docker-entrypoint.sh
COPY "$PWD/joplin" /app/joplin

ENV PORT ${PORT:-80}
EXPOSE $PORT

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ./joplin/manage.py runserver 0.0.0.0:$PORT
