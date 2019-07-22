# Joplin - CMS for the City of Austin

Joplin is the Authoring Interface for adding and editing content for alpha.austin.gov.

<img src="/README/authoring_interface.png" align="middle" width="500" >

<br>The public facing frontend (Janis) displays the content that is published in Joplin.

<img src="/README/janis.png" align="middle" width="500" >

<br>Joplin is built using Wagtail, a Content Management System (CMS) using Python's django framework.

## Index

-   [How to Run Locally](#how-to-run-locally)
-   [Updating the Data Model](#updating-the-data-model)
-   [CircleCI Deployments](#circleci-deployments)
-   [Useful Commands](#useful-commands)
-   [Debugging With Pycharm](#debugging-with-pycharm)
-   [Design](#design)
-   [Misc](#misc)

---

## How to Run Locally

First, install docker (version 18.09 or greater) and clone this repo.

**Run without data**

```
./scripts/serve-local.sh
```

-   This will get you started with one admin user and no data.
-   It will automatically run all django migrations.
-   It will start up 3 docker containers: `joplin_app_1` (for running the CMS web server), `joplin_assets_1` (for managing assets), and `joplin_db_1` (for the postgres database).
-   Viewing your docker logs, you can tell that your server is running successfully when you see these listeners:
    <img src="/README/server_success.png" align="middle" height="70" >
-   Your Joplin instance will be accessible at http://localhost:8000/admin with the credentials user: `admin@austintexas.io`, pw: `x`

**Run with data**

```
LOAD_DATA="on" ./scripts/serve-local.sh
```
-   This will add some test content (from `joplin/db/system-generated/seeding.datadump.json`)
-   Images are also not stored in this repo, and can instead be downloaded using `./scripts/download-media.sh`. This will parse a backup file from the db/smuggler directory and place all referenced images into the local media folder.

**Drop Existing DB**

```
DROP_DB=on ./scripts/serve-local.sh
```

**Drop DB, run with fresh data**

```
RELOAD_DATA=on ./scripts/serve-local.sh
```
-   LOAD_DATA=on + DROP_DB=on

**Run with Janis**

```
JANIS="on" ./scripts/serve-local.sh
```

-   Runs with the "janis:local" image built on your machine.
-   Can be combined with any other args.

**Run + Rebuild without cached image layer**

If something goes wrong with your docker builds and you want to start over without any cached layers, you can run:

```
HARD_REBUILD="on" ./scripts/serve-local.sh
```

-   `LOAD_DATA="on"` can also be used with `HARD_REBUILD="on"`
-   It takes 90 seconds to do a HARD_REBUILD.
-   If worse comes to worse, you can always delete your local joplin docker images with `docker rmi`.

**Run undockerized**

You might prefer to run the Django app on your host computer to enable better access to debugging tools. This script will still run joplin_assets and joplin_db on docker containers, but will run a django `runserver` command directly on your host computer.

```
pipenv install --requirements deploy/requirements.txt
sh scripts/undockered.sh
```

**Run with custom smuggler data**

If you don't want to load the default data used in `LOAD_DATA="on"`, you have to ability to source data from any environment you'd like using a django plugin called [smuggler](https://github.com/semente/django-smuggler).

To load in data from smuggler follow these steps.

1. Download a json datadump from the Joplin deployment of your choosing by visiting `[joplin URL]/django-admin/dump`.
2. Place your datadump in the smuggler fixtures directory `joplin/db/smuggler`
3. Start a data-less empty local Joplin instance with `./scripts/serve-local.sh`.
    - Note! If you previously loaded data locally, make sure to delete your existing `joplin_db_1` container before this step.
4. Go to your local Joplin's smuggler interface at http://localhost:8000/django-admin/load/. Select the data file that you want to load.
5. At this point the database should be populated, but any media used on the site will be broken, to fix this run: `./scripts/download-media.sh`

**Access Local DB**

`psql postgres://joplin@localhost:5433/joplin`

The database defaults to version 10 of postgres. No password is set up, since there is no security needed for a local environment. To connect, use the localhost at the standard PostgreSQL (5432) port where the container is mapped to listen for connections all without a password, the user and database name is 'joplin'. To manage the database, you should be able to use your favorite DB admin tool (ie. TablePlus, DBeaver, DataGrip, etc).

It runs on PORT 5433 to avoid port conflicts with your host's default postgres port.

Note: The containers are not built at the same time; for this purpose, joplin will wait and display a 'database not available' message in a loop until the database is up and ready. This is because the DB container takes a little longer to build and set up locally, and joplin has to wait before it can run the django migrations locally.

**Handling schema migration conflict**

Sometimes, you may run `./scripts/serve-local.sh` and find that the joplin container cannot run due to a migration conflict.

If you check the log, you might see an error like this:

```
app_1     | CommandError: Conflicting migrations detected; multiple leaf nodes in the migration graph: (0073_auto_20190604_2124, 0069_auto_20190530_2220 in base).
app_1     | To fix them run 'python manage.py makemigrations --merge'
```

In that case, to fix the error run:

```
./scripts/run-handle-migration-conflicts.sh
```

This will run `makemigrations` with the --merge flag, and should do a good job handling simple conflicts.

See more:
https://docs.djangoproject.com/en/2.2/topics/migrations/

---

## Updating the Data Model

1. Have a local Joplin instance running (probably populated with data).
2. Update your data model in `joplin/base/models.py`.
3. Make a new migration with:
    - `docker exec -it joplin_app_1 python joplin/manage.py makemigrations`
4. Run that migration with:
    - `docker exec -it joplin_app_1 python joplin/manage.py migrate`
5. Test that your migration works with
    - `./scripts/migration-test.sh`    

**About migration-test script**

The migration-test script makes sure that your migration changes will work even when they are applied to a database running the last migration. This is basically a dry run of a merge to the master branch of Joplin. If they do work, then the script will create a new datadump (to be used by `LOAD_DATA="on"`) with the new migrations applied. This will prevent future datadump schema version conflicts (which will happen if your datadump is from a different migration version than the Joplin instance its going into).

Options:
  - "LOAD_PROD_DATA=on" will source data from production and build migrations from "cityofaustin/joplin-app:production-latest" image
    - Default is to source data from current seeding.datadump.json and build migrations from "cityofaustin/joplin-app:master-latest" image
  - "DOCKER_TAG_DB_BUILD=[x]" will build initial migrations from the docker image of your choice. Potentially could be used if you intend to merge into a branch other than master.
  - "JANIS=on" will automatically spin up a Janis container for you. Note: you must have a "janis:local" image available locally.

Here's what `migration-test.sh` does at a high level:

1. Creates a database from the last working Joplin migration
    - This is accomplished by running Joplin migrations and data loading from the joplin_app image tagged as `cityofaustin/joplin_app:master-latest` from the City of Austin's dockerhub.
    - Note: if you aren't intending to fork from/merge into the latest master branch, you can manually plug in your own `DOCKER_TAG_DB_BUILD` to test how you migrations work against a different build by running `DOCKER_TAG_DB_BUILD=[joplin-app:some-tag] migration-test.sh`.
2. Runs your new migrations on the old database
    - The previous joplin_app container shuts down (but the joplin_db stays up). Now a new joplin_app container (built from your local Joplin directory, tagged as "joplin_app:local") runs against the old joplin_db. The new migrations are automatically applied through joplin_app's entrypoint.
3. Spins up a local Janis and Joplin for you to test manually.
    - If you pass `JANIS=on ./scripts/migration-test.sh` then it will automatically spin up a Janis image using your own janis:local image. Otherwise, at this step you can manually start a Janis instance using another method.
    - Make sure that Joplin and Janis work as expected and that nothing breaks on Janis.
    - A command line prompt will ask if the migration worked. If you enter "y", then a new datadump fixture will replace the old seeing.datadump.json fixture in joplin/db/system-generated. If you enter "n", then the migration_test containers will shut down and not replace your datadump fixture.

## CircleCI Deployments

We use CircleCI to manage and customize our deployments to our cloud infrastructure. Important files to consider:

`.circleci/config.yml`

This file contains the stages and commands to execute, and the order of execution. It also contains the conditions under which a deployment can happen.

`/circleci/docker`

The contains the docker images used during circleci builds. The `joplin-ci-build` image is for the build job (BUILDKIT=1 docker builds are very particular and need a special image and deployment process as of 05/2019). `joplin-ci-deploy` is used for every other job.

Builds for these images are done manually as needed and then stored in the cityofaustin dockerhub repo. You can build and push a new image by following these steps:

```
SHA=$(git rev-parse HEAD)
docker build -f .circleci/docker/joplin-ci-build.Dockerfile -t "cityofaustin/joplin-ci-build:${SHA:0:7}" .circleci/
docker push cityofaustin/joplin-ci-build:${SHA:0:7}
```

Then update the image tags in `/circleci/config.yml` to use your new git commit SHA tag.

**Steps**

CircleCI will run the deployment workflow for every branch. Certain branches will have different steps applied to them.

The deployment is handled in four different stages, for each job circleci will create a new container (with a temporal (ephemeral) file system) and run all the operations as indicated per stage.

**1. test**

`.circleci/scripts/cli_test.sh`

At the moment the pre-deployment tests only check whether the AWS & Heroku CLI tools have been installed and are properly running.

**2. backup_database**

`.circleci/scripts/backup_database.sh`

If deploying on master or production, we first take a backup of the database and store it in S3 for disaster recovery. The backup file name is comprised of these values:

-   The name of the application
-   The timestamp
-   The SHA of the latest commit
-   The name of the latest django migration

Once the name is generated then it proceeds to generate a full URL link where the final file will be stored in S3. It connects to the database and generates a full backup and automatically saves it to S3 using the established nomenclature.

**3. create_review_app**

`.circleci/scripts/create_review_app.sh`

Builds infrastructure for a new heroku app. This step is only done for PR/Review/Dev branches because staging and production branches already have heroku apps in place.

**4. build_and_release**

`.circleci/scripts/build.sh`
Builds the Joplin docker image and pushes to cityofaustin's dockerhub repo and the heroku app.

`.circleci/scripts/release.sh`

Releases the docker image pushed to heroku in the previous step. This is what actually deploys the image to heroku.

`.circleci/scripts/migrate.sh`

Heroku Docker entrypoints time out at 60 seconds. So django migrations and data loading need to be initiated by invoking the `docker-entrypoint.sh` script manually.

The migration process currently consists of 3 commands:

-   `python ./joplin/manage.py migrate` - This command will trigger the django migration process. It runs for all instances on the Cloud: PRs, Staging and Production.
-   `python ./joplin/manage.py loaddata` - This command will import the latest datadump in `joplin/db/system-generated`. This only happens for PR branches.
-   `python ./joplin/manage.py collectstatic` - Triggers the collect static process which only takes care of wagtail and certain images. This only runs for staging and production.

---

## Useful Commands

-   Shut down all joplin containers:
    -   `source scripts/docker-helpers.sh; stop_project_containers joplin`
-   Delete all joplin containers:
    -   `scripts/docker-helpers.sh; delete_project_containers joplin`
-   Create New App:
    -   ```
        APP_NAME=app_name_goes_here
        docker exec joplin /bin/bash -c "mkdir -p \"$APP_NAME\" && cd joplin && python manage.py startapp \"$APP_NAME\""
        ```
-   Access the Graphql API
    -   `localhost:8000/api/graphiql`
-   Troubleshooting:

    -   Clean up older docker images and containers and rebuild the new application if necessary:
    -   ```
        # Assuming you only have joplin containers running, remove all containers first:
        docker rm $(docker container ls -aq);

        # Delete orphan (dangling) images only:
        docker rmi $(docker image ls -aq -f "dangling=true");

        # Then Rebuild (be sure to have the heroku cli installed in your machine)
        REBUILD=on ./scripts/serve-local.sh
        ```

---

## Debugging with Pycharm

1. Run `sh scripts/undockered.sh` to initialize an undockered Joplin instance. This will run your initial data migration and seeding for you. It will also spin up joplin_db and joplin_assets containers. These are steps that our Pycharm debugging script can't do on its own.
2. Shut down `^C` your undockered Joplin runserver. The joplin_db and joplin_assets containers should still be running.
3. Open Pycharm.
4. Open your 'Undockered Joplin' Run Configuration `Run > Debug 'Undockered Joplin'`. This run configuration should be git committed in your .idea/ folder. It will run a Joplin `runserver` command with the benefit of Pycharm's debugger. 

---

## Design

#### icons

To get a full set of icons that Wagtail has available you'll need to upload [Wagtail's icomoon icon definitions](https://raw.githubusercontent.com/wagtail/wagtail/master/wagtail/admin/static_src/wagtailadmin/fonts/wagtail-icomoon.json) to the [icomoon web app](https://icomoon.io/app/). Make sure you're uploading the icon definitions for the version of wagtail we're using.

#### Adding Scripts/Styles

We're using webpack to bundle syles and scripts, and webpack_loader to include them in our templates. To create a new bundle it should be defined as an entry in `webpack.build.js` and `webpack.dev.js`, then included in a template using `{% load render_bundle from webpack_loader %}` and `{% render_bundle 'YOUR_BUNDLE_NAME_HERE' %}`.

---

## Misc

#### Static File Uploads

The master branch (staging app, joplin-staging.herokuapp.com) and production branch (production app, joplin-production.herokuapp.com) upload static files to an S3 bucket (both share the same bucket), but have separate databases.

#### Rebuilding Janis on Heroku when new pages are published

You can set environment variables to get Heroku to rebuild Janis when pages are published. For example, to rebuild `janis-staging` on heroku when a page is published locally, run things like this:

```
HEROKU_JANIS_APP_NAME=janis-staging ./scripts/serve-local.sh
```
