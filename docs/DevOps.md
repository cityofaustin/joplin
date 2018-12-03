# DevOps - Joplin

Previously, our development and production environments were very limited. Data was not permanently saved in local instances or in the cloud, and did not allow to efficiently import data from one environment to another. The deployment to from local to cloud instances did not rely on best practices for large production environments, and did not have the necessary mechanisms to scale up the platform. While it was great for local development, it was not going to allow the growth of the platform or the rest of the project.

A new development pipeline needed to be implemented with enough roboustness to handle the necessary complexity, and also to provide full accountability and contingency mechanisms. The main goal was to create as much consistency and compatibility between environments as possible, in other words, the code in the local environment should be as identical as production, and the database engine should be the exact same version as the one in production, so that way they both are fully compatible.

### General Architecture

```sequence
Note left of Local: "Environment \n -------------- \nDB Attachment"
"Local"->GitHub: "Push/Pull Code"
GitHub->"Local": ""
Note right of GitHub: "Travis-CI Automatic \nDeployments on Update"
GitHub-->"Preview Apps": ""
GitHub-->Master: ""
GitHub-->Production: ""
```

We currently have four separate environments, all have the same components in common. All use the same application code base (repository), they all use Docker to build and deploy the application, and all run with a separate PostgreSQL instance, either locally or in the cloud. This architecture is meant to allow a more efficient development process, but also to allow the expansion of the platform as needed in terms of developing new tools, external services, scaling up for increased traffic, etc.

#####Local

The local environment will be built and run automatically using the tools described in the Joplin project documentation. The start-up scripts will build all necessary environments (application, database, and static file servers). It is possible to import/export the data between other environments.

#####Pull Request

Pull requests (also known as Review Apps) are run on the cloud, they are automatically created after a pull request is created. First, the new code branch in the local environment has to be pushed to the joplin repository, where it is an option to create a Pull Request in GitHub. Once the pull request is created, the app will be automatically built.  See deployment process for details.

#####Master (staging)

The master branch (also known as staging), is our development code branch. All new features and new development is made from and against this branch. Once a pull request is built and reviewd, it can be merged. The pipeline will automatically update and re-build the application for any new code pushed into the master branch.

#####Production 

This is our production environment and it is built off of the production branch in GitHub. There is no need to promote staging into production, but rather we now simply have to merge the changes from master into production (after a full team review). 

About the platform, we use the following providers:

#####Heroku

We use heroku to deploy our applications, it is currently our cloud hosting environment. It provides several tools to automate and expedite the build process and performance scaling.

#####AWS

We use AWS S3 in multiple ways, most importantly it allows us to store a virtually infinite amount of files for staging and production, it also allows to reduce the pressure in a high volume of traffic on the site. We also store the backups generated for nearly all of our environments.

#####Travis CI

We use Travis CI to customize the deployment between different environments, it allows us to have different stages where we can improve the quality of the application by pre-testing the deployment, create backups, monitor the build & release stage, and to run long database processes if needed. There is no limit in the level of customization needed for a project. 

### Code Deployments

Currently, our code deployments are taken care of by GitHub, Heroku and TravisCI. Any new feature branch can be created freely from master and pushed to github, any new code pushed to a new branch will not be built by Heroku or Travis CI. Once the code is ready to be reviewed you may create a Pull Request (PR) on GitHub. Only PRs, master and the production branches will be automatically built on the cloud, once new code is pushed to any of them a webhook is trigged on TravisCI to build a new application with its own database on Heroku. This process usually takes around 10-50 minutes. You can see the status of the deployment in [Travis-CI.org (click here)](https://travis-ci.org/cityofaustin/joplin), if necessary, log in using your GitHub account.

##### Where is the deployment implemented?

We currently use Travis CI to manage and customize our deployments to our cloud infrastructure, there are two files that govern this process:

`.travis.yml` - This file contains the stages and commands to execute, and the order of execution. It also contains the conditions under which a deployment can happen.

`.travis/heroku-helper.sh` - This file is a helper for our current infrastructure provider, it allows to create applications for review, create backups, databases, deploy to PRs, staging and production applications, etc. All the logic and routines are contained here.

##### Pull Requests (Review Apps)

PRs are also known as Review Apps, but they are different from Master/Production apps:

1. PR apps have an ephemeral (temporal) file system and database, meaning that any files or any changes uploaded to the app will be cleared when new code is pushed to the PR, the same happens to the database. This is because Travis will build a brand-new container, register that container on Heroku, and then deploy that container to the cloud. If successful, Travis will run a separate process to run the data migration.
2. Migrations on PRs will wipe out the current database. A backup is created and put into a bucket prior to the rebuilding of the app, for details see the Deployment Process section.

You may deploy as many PRs, update and rebuild as many times as you need, these will not affect master or staging in any way.

##### Master (staging) & Production

Master and Production will be rebuilt automatically once new code is pushed to either, but their file system is shared on the cloud via S3. Both Master and Production share an S3 bucket, which helps upload files for staging without affecting production; however, it requires extra attention when deleting files. For details on the deployment process and data migration see the Deployment Process section below.

Database:

Master (staging) & production have separate databases. You can see the access details on the Heroku Dashboard. 

Deployment Rules:

1. Create a PR branch and have it ready for review. It must be a successful deployment and the live demo has to be reviewable by any other team member.
2. Wait for a Q/A review and approval from at least 1 senior developer.
3. **In Production, any new code must be production-ready before it is commited. Hot-fixes or any type of direct commits are not permitted. Production deployments require a full-team review.**



#### Deployment Process

The deployment currently relies on four different stages:

**1. Testing Stage**

Here all pertinent testing in relation to the app and the deployment of the app takes place. This stage is ever-evolving and updated frequently. Among the tests performed are: making sure that deployment tools are installed and running, making sure we have access to all the resources needed to build the application, for example:

- Prints current-build environment variables for debugging.
- AWS CLI
- AWS user policy & permissions
- Heroku CLI
- Script functions in `.travis/heroku-helper.sh`

If the tests fail, the deployment will be cancelled and marked as Failed for debugging. An email notification with a faliure message will be sent. 

**2. Database Backup Stage** 

This is a default part of the process, every time new code is pushed (to a PR, master  or production) a new backup will be created, compressed and uploaded to an S3 bucket, regardless if it succeeds or if it fails. The name of the backup file includes the following information:

- The name of the application
- The name of the branch
- The date/time of its creation
- The latest django migration number
- The commit id number

This process will check if the backup was in fact created, if it cannot find the new file the deployment will be cancelled and marked as Failed for debugging. An email notification with a faliure message will be sent.

**3. Build & Release Stage**

The build stage will relies on a few steps and environment variables to determine how to build the application and where to deploy the newly built application, but in general terms it will run in this order:

1. Database Cleanup
   1. Removes any ownership entries in the PSQL dump present in the source code.
   2. Copies the clean PSQL dumps into S3 for loading if needed.
   3. Clean PSQL dumps will be part of the newly built docker image.
2. Create PR app (in Heroku)
   1. Determines if current build is a PR and if the application is already built. If already built, it moves on to the next step.
   2. It attaches necessary environment variables, these are set up in Travis > Settings. The deployment process will copy the values from those settings, and it will assign the values to the new application. The name of the variables in Travis are nearly identical as the variables set up and visible from the Heroku dashboard, where you can see them in the application settings, then click "Reveal Config Vars".
   3. If it does not have a Database, create it and attach to new application.
   4. Attaches the new PR application into the joplin pipeline with the rest of the other review apps, master (staging) and production applications.
3. Build step:
   1. Download Source from repo. This is done automatically by TravisCI, it will clone the joplin repository by default, and it will follow the instructions in `.travis.yml`. 
   2. Log in to the heroku container registry. This is important in order to be able to upload our docker images to heroku, without this it is best not to proceed.
   3. Build the container. This is accomplished by through the normal `docker build` mechanism which will read the `Dockerfile` and follow the instrucctions therein.
   4. Tag the container for release with an image name. The tagging is necessary to identify the image by name and associate it to an app. Once the app gets released, it will know what image to use.
   5. Push the container to release. We finally upload the image to the heroku repository.
4. Release Step
   1. Determine image id for current branch.
   2. Make an API call to release & run the container. 

If there is an error in any of these steps, the deployment will be cancelled and marked as Failed for debugging. An email notification with a faliure message will be sent.

**4. Data & File Migration Stage**

Our data & file migration is run in this stage, it can take up a few minutes depending on how much data there is to be migrated. The process is handled by running an external dyno on heroku. The migration process currently consists of 3 commands:

- `python ./joplin/manage.py migrate` - This command will trigger the django migration process. It runs for all instances on the Cloud: PRs, Staging and Production.
- `python ./joplin/manage.py dbimport` - This command will import the latest instance database backup in folder. This only happens for PR branches.
- `python ./joplin/manage.py collectstatic` - Triggers the collect static process which only takes care of wagtail and certain images. This only runs for staging and production.

The process is not perfect and it is bound to struggle at any point of the deployment, feel free to document any issues you see so that the process can be improved.

For every step, the migration will check if there have been any errors, if there are it will print a code "MIGRATION_EXIT_STATUS_ERROR" that will trigger the entire process to stop and mark the deployment as failed, which will send an email to all development stakeholders. A full output of the error will be available will be available in Travis.

### Environment Variables

The following variables are needed for all PRs, master and production applications:

- `DEPLOYMENT_MODE` This variable helps the application determine what configuration to use for storage or database settings. This variable is created and assigned automatically by the deployment process.

  - `REVIEW`: Review Apps (PRs)
  - `STAGING`: For the master application
  - `PRODUCTION`: For the production application 

  ```
  DEPLOYMENT_MODE=REVIEW|STAGING|PRODUCTION
  ```

- `APPLICATION_NAME`: the name of the application, this helps to determine where to place the backups and the file names of the backup. This variable is created and assigned automatically by the deployment process. The values are (for example):

  - `joplin-staging-pr-181`: PR number 181
  - `joplin-staging`: The name of the master application.
  - `joplin`: The name of the production application.

  ```
  APPLICATION_NAME=joplin-staging-pr-181 (example)
  ```

- `AWS_S3_USER`: The name of the AWS user with s3 access, this user is created in AWS IAM, and it is given limited privileges to only be able to access the specific buckets to this project and only to upload new files. This variable is created by the deployment process and it copies the value from Travis CI Env. Variable `AWS_S3_USER_DEFAULT` 

  ```
  AWS_S3_USER=joplin-aws-user (example)
  ```

- AWS_S3_KEYID: The private key id of the aws s3 user. This is the private key id as taken from AWS IAM. This variable is created by the deployment process and copies the value from Travis CI Env. Variable `AWS_ACCESS_KEY_ID` 

  ```
  AWS_S3_KEYID=AFIWN1UXAU02GJGKLPDD (example)
  ```

- AWS_S3_ACCESSKEY: The secret access key of the was s3 user. This is the private key of the aws s3 user. This variable is created by the deployment process and copies the value from Travis CI Env. Variable ` AWS_SECRET_ACCESS_KEY` 

  ```
  AWS_S3_ACCESSKEY=tb29Z54p8YDo4AnV342QN3U362Ph29Ah9jrNC9am (example)
  ```

- AWS_S3_BUCKET: The name of the bucket to be used to store all the images, static files. This value should be the same between master (staging) and production. This variable is created by the deployment process and copies the value from Travis CI Env. Variable `AWS_BUCKET_DEFAULT` 

  ```
  AWS_S3_BUCKET=joplin-aws-bucket (example)
  ```

- AWS_S3_BUCKET_ARCHIVE: The name of the bucket to used as an archive, where all the database backups will be stored. This variable is created by the deployment process and copies the value from Travis CI Env. Variable `AWS_BUCKET_ARCHIVE_DEFAULT` 

  ```
  AWS_S3_BUCKET_ARCHIVE=joplin-aws-bucket-archive (example)
  ```

- AWS_S3_BUCKET_ARCHIVE_LOCATION: The name of the folder within the archive bucket where the backups will be placed. This variable is created by the deployment process and copies the value from Travis CI Env. Variable  `AWS_S3_BUCKET_ARCHIVE_LOCATION_DEFAULT`

  ```
  AWS_S3_BUCKET_ARCHIVE_LOCATION=backups (example)
  ```

### Helper Functions

The deployment process relies on a series of different functions implemented in the file `.travis/heroku-helper.sh`. Here is where all the customization has been implemented. Depending on the current cloud provider, a new script may have to be implemented. For this particular script, these are the functions that customize the process:

- `helper_halt_deployment`- Prints error message and stops deployment entirely by calling the `travis_terminate` function within the Travis CI execution library.
- `helper_internal_validation` The purpose of this function is to make sure there is a branch name specified before the processes begin. It is also used to test the rest of the functions have been initialized correctly by using the branch name `travis-ci-internal-test` this will indicate certain functions being called that there is no need to fully execute the command.
- `joplin_print_header` It prints a header that makes it easier to read in the deployment logs in TravisCI.
- `joplin_app_exists ` Returns "true" if the name of an application exists within the heroku platform.
- `joplin_app_database_attached`- Returns "true" if the application in question has a postgresql database attached to it.
- `joplin_log` - This function is a simple mechanism to log events, information or actions into the output text in Travis CI, this is only meant for additional debugging.
- `joplin_is_numeric` - A helper function that uses a regular expression if the input text is numeric.
- `joplin_parse_commit_message` - This function was necessary during the development process to do things such as forcing specific PR numbers, changing pipeline names, forcing an application name, etc. The purpose of this application is to parse commands within a commit message in Git, this to allow the customization of the process. While this function is not necessary, it remains here due to development potential and usefulness for debugging the deployment process.
- `joplin_attach_heroku_database` - This function creates a postgres database add-on for an exsisting application.
- `joplin_tag_application`- Adds all the necessary environment variables to an existing application.
- `joplin_create_heroku_preview_app` - Builds a new review application and attaches the app to a pipeline with (review) status.
- `joplin_resolve_heroku_appname` - Returns the name of the application in heroku given the branch name.
- `retrieve_latest_django_mid`- Returns the latest base migration id in Django.
- `heroku_backup_upload_check` - Halts Deployment if the backup cannot be found in the S3 bucket.
- `joplin_reset_db_backups_owner` - Retrieves correct DB Owner ID and Resets ALTER TABLE lines to OWNER TO  '<CORRECT OWNER HERE>'
- `joplin_remove_db_ownership` - Removes all ownership lines from a PSQL file
- `joplin_copy_local_restorepoint_backups` - Copies the local database files (obtained from github) into the S3 for use in the migration process.
- `joplin_backup_database` - Creates a database backup of a running heroku app.
- `joplin_create_pr_app` - Creates a pull request application and puts it in the specified pipeline.
- `joplin_build`- Builds the docker container and pushes the image to the heroku repository where it can be tagged to an app and released.
- `joplin_release`- Calls the release function for a specific image to a specific application.
- `joplin_migrate` - Runs the migration process in a heroku dyno on the target application.
- `helper_test`- Runs a series of test functions to make sure they are ready to execute.



This is a general overview of the entire pipeline process; while it currently relies heavily on AWS and Heroku, it can be customized for any other cloud provider. Most of the logic can be reused and adapted to any other project.