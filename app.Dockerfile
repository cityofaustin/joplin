########################################################
# joplin-common

FROM cityofaustin/joplin-base:8a6c8a5 as joplin-common

# Install Python dependencies
COPY "$PWD/Pipfile"
RUN pipenv lock --requirements > ./requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check --requirement ./requirements.txt

# Set Working Directory
RUN mkdir /app
WORKDIR /app

# Copy over project files
COPY "$PWD/joplin" /app/joplin
COPY "$PWD/media" /app
COPY "$PWD/scripts" /app/scripts
COPY "$PWD/docker-entrypoint.sh" /app/docker-entrypoint.sh

########################################################
# joplin-common => joplin-local

FROM joplin-common as joplin-local

ENV DEPLOYMENT_MODE "LOCAL"

# Run Migrations
ENTRYPOINT ["./docker-entrypoint.sh"]

# Start the Joplin server
# we add an extra timeout and debug level to be generous with our server log
CMD ["gunicorn", "joplin.wsgi:application", "--pythonpath", "/app/joplin", "--reload", "--timeout=190", "--log-level=DEBUG"]

########################################################
# joplin-base => joplin-deployed

FROM joplin-base as joplin-deployed

# Install nodejs dependencies
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get update; apt-get -y install nodejs
RUN npm install --global yarn

# Build nodejs dependencies for deployed builds
WORKDIR /app/joplin
RUN npm rebuild node-sass
RUN yarn; yarn build
WORKDIR /app

# Entrypoint must be executed manually since heroku has a 60 second time limit for entrypoint scripts
# Start the Joplin server
CMD ["gunicorn", "joplin.wsgi:application", "--pythonpath", "/app/joplin"]

########################################################
# joplin-base => joplin-deployed => joplin-review

FROM joplin-deployed as joplin-review

ENV DEPLOYMENT_MODE "REVIEW"

########################################################
# joplin-base => joplin-deployed => joplin-staging

FROM joplin-deployed as joplin-staging

ENV DEPLOYMENT_MODE "STAGING"

########################################################
# joplin-base => joplin-deployed => joplin-prod

FROM joplin-deployed as joplin-prod

ENV DEPLOYMENT_MODE "PRODUCTION"
