FROM node:10.8.0-slim

RUN mkdir /app
WORKDIR /app

COPY "$PWD/joplin" /app/joplin
COPY "$PWD/docker-entrypoint.assets.sh" /app/docker-entrypoint.assets.sh

ENTRYPOINT ["./docker-entrypoint.assets.sh"]
