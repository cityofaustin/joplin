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

**NOTE** You may encounter issues with the script exiting prematurely if you haven't installed the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) and run `heroku login`.


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

## Update: New deployment pipeline

The team is currently working on a new deployment pipeline using best practices for continuous integration, backups, data persistence and deployment accountability. As of this moment only the local, staging and production environments have data persistence, while PR (review) apps are still using Heroku's (non-persisted) pipeline until new updates are made in the next few weeks.

Locally, the latest version of the application no longer uses SQLite. Instead, it initializes a separate container with a PostgreSQL server where the data is saved, this is to maintain our development environment as identical as possible to the production environments. Before you launch the build command, be sure to clean up older docker images and containers and rebuild the new application if necessary:

```
# Assuming you only have joplin containers running, remove all containers first:
docker rm $(docker container ls -aq);

# Delete orphan (dangling) images only:
docker rmi $(docker image ls -aq -f "dangling=true");

# Then Rebuild (be sure to have the heroku cli installed in your machine)
REBUILD=on ./scripts/serve-local.sh
```

The new build process will create a service (group) of containers:

1. joplindb (PostgreSQL)
2. joplinassets (assets)
3. joplin (backend)

The database defaults to version 10 (latest) of postgres. No password is set up, since there is no security needed for a local environment. To connect, use the localhost at the standard PostgreSQL (5432)  port where the container is mapped to listen for connections all without a password, the user and database name is 'joplin'. To manage the database, you should be able to use your favorite DB admin tool (ie. TablePlus, DBeaver, DataGrip, etc). Be sure you are not running a local PostgreSQL server prior to building the containers. Example connection string: `postgres://joplin@localhost:5432/joplin`

The master branch (staging app, joplin-staging.herokuapp.com) and production branch (production app, joplin-production.herokuapp.com) upload static files to an S3 bucket (both share the same bucket), but have separate databases.  

Note: The containers are not built uniformly; for this purpose, joplin will wait and display a 'database not available' message in a loop until the database is up and ready. This is because the DB container takes a little longer to build and set up locally, and jopling has to wait before it can run the django migrations locally.



## Create new app

```
APP_NAME=app_name_goes_here
docker exec joplin /bin/bash -c "mkdir -p \"$APP_NAME\" && cd joplin && python manage.py startapp \"$APP_NAME\""
```


## Design
#### icons
To get a full set of icons that Wagtail has available you'll need to upload [Wagtail's icomoon icon definitions](
https://raw.githubusercontent.com/wagtail/wagtail/master/wagtail/admin/static_src/wagtailadmin/fonts/wagtail-icomoon.json) to the [icomoon web app](https://icomoon.io/app/). Make sure you're uploading the icon definitions for the version of wagtail we're using.

#### Adding Scripts/Styles
We're using webpack to bundle syles and scripts, and webpack_loader to include them in our templates. To create a new bundle it should be defined as an entry in `webpack.build.js` and `webpack.dev.js`, then included in a template using `{% load render_bundle from webpack_loader %}` and `{% render_bundle 'YOUR_BUNDLE_NAME_HERE' %}`.
