FROM python:3.6.4-slim-stretch

COPY /deploy/requirements.txt /deploy/requirements.txt
RUN pip install --no-cache-dir -r /deploy/requirements.txt

RUN mkdir /app
WORKDIR /app

# TODO: Don't copy fixtures
COPY "$PWD/fixtures" /app/fixtures

COPY "$PWD/docker-entrypoint.sh" /app/docker-entrypoint.sh
COPY "$PWD/joplin" /app/joplin
COPY "$PWD/media" /app/media

ENV PYTHONUNBUFFERED=0
ENV WEB_CONCURRENCY=4
ENV PORT ${PORT:-80}
EXPOSE $PORT

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "joplin.wsgi:application", "--pythonpath", "/app/joplin"]
