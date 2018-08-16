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

**NOTE** The first time docker-compose runs it builds new images, every time after the images are not rebuilt. To clear the cache and rebuild add `REBUILD=on`.

```
REBUILD=on ./scripts/serve-local.sh
```

### Rebuild Janis on Heroku when new pages are published

You can set environment variables to get Heroku to rebuild Janis when pages are published. For example, to rebuild `janis-staging` on heroku when a page is published locally, run things like this:

```
HEROKU_JANIS_APP_NAME=janis-staging ./scripts/serve-local.sh
```

`HEROKU_KEY` is read from the Heroku CLI. If you don't have the CLI installed or it's unconfigured, you'll need to set the `HEROKU_KEY` environment variable when running. You can check to see if you're logged in by running `heroku auth:whoami`.

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

## Update database from yaml file

As you make edits to yamls files, you will need to run the following command while the server is running:

```
docker exec --interactive --tty joplin python ./joplin/manage.py loadcontent fixtures/name-of-fixture.yaml
```


## Create new app

```
APP_NAME=app_name_goes_here
docker exec joplin /bin/bash -c "mkdir -p \"$APP_NAME\" && cd joplin && python manage.py startapp \"$APP_NAME\""
```


## Design
#### icons
To get a full set of icons that Wagtail has available you'll need to upload [Wagtail's icomoon icon definitions](
https://raw.githubusercontent.com/wagtail/wagtail/master/wagtail/admin/static_src/wagtailadmin/fonts/wagtail-icomoon.json) to the [icomoon web app](https://icomoon.io/app/). Make sure you're uploading the icon definitions for the version of wagtail we're using.
