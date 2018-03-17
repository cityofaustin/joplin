# Joplin - CMS for the City of Austin

This is where you'll find the CMS for the City of Austin and atx.gov

## Background

If you wanna do stuff in the CMS, then you will need these commands.

## Run locally

Make sure you have docker installed, then run:

```
./scripts/serve-local.sh
```

**NOTE** Fixture data is automatically loaded the first time you run the server. Add `LOAD_DATA=on` if you ever need to start with a fresh copy.

```
LOAD_DATA=on ./scripts/serve-local.sh
```

#### Access the admin

You can access the admin at `localhost:8000/admin` with the credentials `admin@austintexas.io`/`x`

#### Access the API

You can access a GraphQL API at `localhost:8000/api/graphiql`


## Create migrations

While the server is running, run the following commands:

```
docker exec --interactive --tty joplin python joplin/manage.py makemigrations
docker exec --interactive --tty joplin python joplin/manage.py migrate
```


## Create new app

```
APP_NAME=app_name_goes_here
docker exec joplin /bin/bash -c "mkdir -p \"$APP_NAME\" && cd joplin && python manage.py startapp \"$APP_NAME\""
```
