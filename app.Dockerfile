########################################################
# joplin-common

FROM cityofaustin/joplin-base:1a73da0 as joplin-common

# Install Python dependencies
COPY "$PWD/Pipfile" ./Pipfile
COPY "$PWD/Pipfile.lock" ./Pipfile.lock
# Create requirements.txt from Pipfile
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
COPY "$PWD/gunicorn.conf.py" /app/gunicorn.conf.py

########################################################
# joplin-common => joplin-local

FROM joplin-common as joplin-local

ENV DEPLOYMENT_MODE "LOCAL"

# Run Migrations
ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["python", "./joplin/manage.py", "runserver", "0.0.0.0:80"]

########################################################
# joplin-common => joplin-deployed

FROM joplin-common as joplin-deployed

# Install nodejs dependencies
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get update; apt-get -y install nodejs
RUN npm install --global yarn

# Build nodejs dependencies for deployed builds
WORKDIR /app/joplin
RUN npm rebuild node-sass
RUN yarn; yarn build
WORKDIR /app

# Start the Joplin server
# Entrypoint must be executed manually since heroku has a 60 second time limit for entrypoint scripts
# we add an extra timeout and debug level to be generous with our server log
CMD ["gunicorn", "-c", "gunicorn.conf.py", "joplin.wsgi:application"]

########################################################
# joplin-common => joplin-deployed => joplin-review

FROM joplin-deployed as joplin-review

ENV DEPLOYMENT_MODE "REVIEW"

########################################################
# joplin-common => joplin-deployed => joplin-staging

FROM joplin-deployed as joplin-staging

ENV DEPLOYMENT_MODE "STAGING"
RUN rm -rf /app/joplin/db

########################################################
# joplin-common => joplin-deployed => joplin-prod

FROM joplin-deployed as joplin-prod

ENV DEPLOYMENT_MODE "PRODUCTION"
RUN rm -rf /app/joplin/db
