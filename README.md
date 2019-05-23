# Joplin - CMS for the City of Austin

Joplin is the Authoring Interface for adding and editing content for alpha.austin.gov.

<img src="/README/authoring_interface.png" align="middle" width="500" >

<br>The public facing frontend (Janis) displays the content that is published in Joplin.

<img src="/README/janis.png" align="middle" width="500" >

<br>Joplin is built using Wagtail, a Content Management System (CMS) using Python's django framework.

## Index
- [How to Run Locally](#how-to-run-locally)
- [Updating the Data Model](#updating-the-data-model)
- [Useful Commands](#useful-commands)
- [Design](#design)
- [Deployments Part 1: New Pipeline](#deployments-part-1-new-pipeline)
- [Deployments Part 2: Travis CI](#deployments-part-2-travis-ci)

---
## How to Run Locally

First, install docker (version 18.09 or greater) and clone this repo.

**Run without data**
```
./scripts/serve-local.sh
```
  - This will get you started with one admin user and no data.
  - It will automatically run all django migrations.
  - It will start up 3 docker containers: `joplin_app_1` (for running the CMS web server), `joplin_assets_1` (for managing assets), and `joplin_db_1` (for the postgres database).
  - Viewing your docker logs, you can tell that your server is running successfully when you see these listeners:
    <img src="/README/server_success.png" align="middle" height="70" >
  - Your Joplin instance will be accessible at http://localhost:8000/admin with the credentials user: `admin@austintexas.io`, pw: `x`

**Run with data**

```
LOAD_DATA="on" ./scripts/serve-local.sh
```
  - This will add some test content (from `joplin/db/system-generated/[latest migration].datadump.json`)
  - Images are also not stored in this repo, and can instead be downloaded using `./scripts/download-media.sh`. This will parse a backup file from the db/smuggler directory and place all referenced images into the local media folder.

**Run + Rebuild without cached image layer**

If something goes wrong with your docker builds and you want to start over without any cached layers, you can run:
```
HARD_REBUILD="on" ./scripts/serve-local.sh
```
  - `LOAD_DATA="on"` can also be used with `HARD_REBUILD="on"`
  - If worse comes to worse, you can always delete your local joplin docker images with `docker rmi`.

**Run with custom smuggler data**

If you don't want to load the default data used in `LOAD_DATA="on"`, you have to ability to source data from any environment you'd like using a django plugin called [smuggler](https://github.com/semente/django-smuggler).

To load in data from smuggler follow these steps.
1. Download a json datadump from the Joplin deployment of your choosing by visiting `[joplin URL]/django-admin/dump`.
2. Place your datadump in the smuggler fixtures directory `joplin/db/smuggler`
3. Start a data-less empty local Joplin instance with `./scripts/serve-local.sh`.
    - Note! If you previously loaded data locally, make sure to delete your existing `joplin_db_1` container before this step.
4. Go to your local Joplin's smuggler interface at http://localhost:8000/django-admin/load/. Select the data file that you want to load.
5. At this point the database should be populated, but any media used on the site will be broken, to fix this run: `./scripts/download-media.sh`

---
## Updating the Data Model

1. Have a local Joplin instance running (populated with data probably).
2. Have an up-to-date "janis:local" docker image available locally.
3. Update your data model in `joplin/base/models.py`.
4. Make a new migration with:
    - `docker exec -it joplin_app_1 python joplin/manage.py makemigrations`
5. Run that migration with:
    - `docker exec -it joplin_app_1 python joplin/manage.py migrate`
6. Test that your migration works with
    - `./scripts/migration-test.sh`    

**About migration-test script**

The migration-test script makes sure that your migration changes will work even when they are applied to a database running the last migration. This is basically a dry run of a merge to the master branch of Joplin. If they do work, then the script will create a new datadump (to be used by `LOAD_DATA="on"`) with the new migrations applied. This will prevent future datadump schema version conflicts (which will happen if your datadump is from a different migration version than the Joplin instance its going into).

Here's what `migration-test.sh` does at a high level:

1. Creates a database from the last working Joplin migration
    - This is accomplished by running Joplin migrations and data loading from the joplin_app image tagged as "cityofaustin/joplin_app:latest-master" from the City of Austin's dockerhub.
2. Runs your new migrations on the old database
    - The previous joplin_app container shuts down (but the joplin_db stays up). Now a new joplin_app container (built from your local Joplin directory, tagged as "joplin_app:local") runs against the old joplin_db. The new migrations are automatically applied through joplin_app's entrypoint.
3. Spins up a local Janis and Joplin for you to test manually.
    - Make sure that Joplin and Janis work as expected and that nothing breaks on Janis.
    - A command line prompt will ask if the migration worked. If you enter "y", then a new datadump fixture will replace the old datadump fixture in joplin/db/system-generated. If you enter "n", then the migration_test containers will shut down and not replace your datadump fixture.

---
## Useful Commands
- Shut down all joplin containers:
  - `source scripts/docker-helpers.sh; stop_project_containers joplin`
- Delete all joplin containers:
  - `scripts/docker-helpers.sh; delete_project_containers joplin`
- Create New App:
  - ```
    APP_NAME=app_name_goes_here
    docker exec joplin /bin/bash -c "mkdir -p \"$APP_NAME\" && cd joplin && python manage.py startapp \"$APP_NAME\""
    ```
- Access the Graphql API
  - `localhost:8000/api/graphiql`

---
## Design

#### icons

To get a full set of icons that Wagtail has available you'll need to upload [Wagtail's icomoon icon definitions](https://raw.githubusercontent.com/wagtail/wagtail/master/wagtail/admin/static_src/wagtailadmin/fonts/wagtail-icomoon.json) to the [icomoon web app](https://icomoon.io/app/). Make sure you're uploading the icon definitions for the version of wagtail we're using.

#### Adding Scripts/Styles

We're using webpack to bundle syles and scripts, and webpack_loader to include them in our templates. To create a new bundle it should be defined as an entry in `webpack.build.js` and `webpack.dev.js`, then included in a template using `{% load render_bundle from webpack_loader %}` and `{% render_bundle 'YOUR_BUNDLE_NAME_HERE' %}`.

---
## Deployments Part 1: New Pipeline

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

**Rebuild Janis on Heroku when new pages are published**

You can set environment variables to get Heroku to rebuild Janis when pages are published. For example, to rebuild `janis-staging` on heroku when a page is published locally, run things like this:

```
HEROKU_JANIS_APP_NAME=janis-staging ./scripts/serve-local.sh
```

## Deployments Part 2: Travis CI

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
