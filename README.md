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

### Managing Local DB

The LOAD_DATA flag will load our backups from the django-dbbackup module. This contains full backups including users, and is not intended to migrate data between environments. In order to keep the size of this repository from ballooning out of control, local backups are made without any page data. In order to load page data locally, visit http://localhost:8000/django-admin/load/ and select a backup from the fixture directory.

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

### Update DB Backups

While the server is running, after running migrations, run the following command:

```
docker exec --interactive --tty joplin python joplin/manage.py dbbackup
```

### Updating the models (for example, adding a new page model)

1. Clear out your docker containers and start fresh with `./scripts/serve-local.sh`
2. Load the current backup `LOAD_DATA=on ./scripts/serve-local.sh`
3. Make your changes to `models.py`
4. Run `makemigrations` and `migrate` - see "Create Migrations" above
5. Make an example page
6. Make a new backup
7. Try starting fresh with your new model/migration/backup

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

The database defaults to version 10 of postgres. No password is set up, since there is no security needed for a local environment. To connect, use the localhost at the standard PostgreSQL (5432) port where the container is mapped to listen for connections all without a password, the user and database name is 'joplin'. To manage the database, you should be able to use your favorite DB admin tool (ie. TablePlus, DBeaver, DataGrip, etc). Be sure you are not running a local PostgreSQL server prior to building the containers. Example connection string: `postgres://joplin@localhost:5432/joplin`

The master branch (staging app, joplin-staging.herokuapp.com) and production branch (production app, joplin-production.herokuapp.com) upload static files to an S3 bucket (both share the same bucket), but have separate databases.

Note: The containers are not built at the same time; for this purpose, joplin will wait and display a 'database not available' message in a loop until the database is up and ready. This is because the DB container takes a little longer to build and set up locally, and joplin has to wait before it can run the django migrations locally.

## Create new app

```
APP_NAME=app_name_goes_here
docker exec joplin /bin/bash -c "mkdir -p \"$APP_NAME\" && cd joplin && python manage.py startapp \"$APP_NAME\""
```

## Design

#### icons

To get a full set of icons that Wagtail has available you'll need to upload [Wagtail's icomoon icon definitions](https://raw.githubusercontent.com/wagtail/wagtail/master/wagtail/admin/static_src/wagtailadmin/fonts/wagtail-icomoon.json) to the [icomoon web app](https://icomoon.io/app/). Make sure you're uploading the icon definitions for the version of wagtail we're using.

#### Adding Scripts/Styles

We're using webpack to bundle syles and scripts, and webpack_loader to include them in our templates. To create a new bundle it should be defined as an entry in `webpack.build.js` and `webpack.dev.js`, then included in a template using `{% load render_bundle from webpack_loader %}` and `{% render_bundle 'YOUR_BUNDLE_NAME_HERE' %}`.

# **Deployments with Travis CI**

We currently use Travis CI to manage and customize our deployments to our cloud infrastructure, there are two files that govern this process:

- .travis.yml

  This file contains the stages and commands to execute, and the order of execution. It also contains the conditions under which a deployment can happen.

- .travis/heroku-helper.sh

  This file is a helper for our current infrastructure provider, it allows to create applications for review, create backups, databases, deploy to PRs, staging and production applications, etc. All the logic and routines are contained here.

**Build Operations**

Travis will detect any changes done to the code on Git, if the change was done to a PR, Master (staging application) or Production (prod application) branch, the process will automatically build and update the applications.

As soon as you push the code to the origin remote Travis will immediately beign the build process. Regular branches are not going to be built.

**Stages**

The deployment is handled in four different stages, for each stage travis will create a new container (with a temporal (ephemeral) file system) and run all the operations as indicated per stage.

**1. Tests**

At the moment the only pre-deployment tests it runs is to make sure that the functions can be called and are ready to be executed. It also tests whether the AWS & Heroku CLI tools have been installed and are properly running.

**2. Database Backup**

The backups stage will first test the AWS cli client is installed in Travis and ready to run, then it will generate a name for the database file that is unique to the current deployment, which includes:

- The name of the application
- The name of the branch
- The date
- The latest django migration number
- The commit id

Once the name is generated then it proceeds to generate a full URL link where the final file will be stored in S3. It connects to the database and generates a full backup and automatically saves it to S3 using the established nomenclature.

Lastly, it will verify the file has been uploaded, if the file is not there then it will cause the deployment to stop completely, and it will show the error in Travis CI.

**3. Build & Release**

First, it will clean up the instance database files located in the joplin/db/backups folder. This is done here because every stage is ephemeral and files are lost between stages.

This is important because the data has to be clean and it should not require special permissions or extensions before it is imported. So it is done here so that the database backup files are cleaned up (if they need to be at all), then they are copied over to s3, then imported automatically if this is a PR branch. Staging and Production do not import instance databases automatically, this is because the current data must not be altered in any way; also, we already have a backup from a previous stage. Any new backups created in the branch will be copied over to its own folder in the s3 backups archive bucket.

**4. Migration**

Our data migration is done in this stage, it can take up a few minutes depending on how much data there is to be migrated. The process is handled by running an external dyno on heroku. The migration process currently consists of 3 commands:

- python ./joplin/manage.py migrate - This command will trigger the django migration process. It runs for all instances on the Cloud: PRs, Staging and Production.
- python ./joplin/manage.py dbimport - This command will import the latest instance database backup in folder. This only happens for PR branches.
- python ./joplin/manage.py collectstatic - Triggers the collect static process which only takes care of wagtail and certain images. This only runs for staging and production.

The process is not perfect and it is bound to struggle at any point of the deployment, feel free to document any issues you see so that the process can be improved.
