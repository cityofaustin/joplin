import os
import sys
import requests

from branch_overrides import branch_overrides

'''
    This is how environment variables get set in our Heroku PR joplin applications.

    Joplin Environment Variables are sourced from 3 places.
    1. CircleCI (vars_from_circleci)
        These environment variables are set in the CircleCI Environment Variables Console
        or in the bash scope of the CircleCI script that runs this function.
    2. default_branch_vars
        These are additional application configs that aren't secret enough to be saved
        in CircleCI's vault. They're also tweaks that are used in PR apps only, but not
        necessarily in Staging or Production builds.
    3. .circleci/vars/branch_overrides.py
        This is where you set environment variables that you want to set specifically for
        your PR branch only.
        The key is your git branch name.
        Within that branch name, set the environment vars that you'd like to override.
        Whatever you set in that object will not contaminate the environment vars of any other branch.
        You're allowed to override any environment var (even ones in vars_from_circleci),
        though you probably don't want to.
        branch_overrides are not required for every branch.
'''
# Dictionary of all environment variables to be set within your Heroku PR App
config = {}

# Set all variables sourced from circleci
vars_from_circleci = [
    "APPNAME",  # .circleci/scripts/helpers.sh
    "AWS_ACCESS_KEY_ID",  # CircleCI
    "AWS_SECRET_ACCESS_KEY",  # CircleCI
    "AWS_S3_USER",  # CircleCI
    "AWS_S3_BUCKET_STATIC",  # CircleCI
    "AWS_S3_BUCKET_ARCHIVE",  # CircleCI
    "AWS_S3_BUCKET_ARCHIVE_LOCATION",  # CircleCI
    "JANIS_URL",  # CircleCI
    "STYLEGUIDE_URL",  # CircleCI
    "CIRCLE_BRANCH",  # CircleCI
    "COA_PUBLISHER_URL",  # CircleCI
    "DJANGO_SECRET_KEY",  # CircleCI
    "ALGOLIA_APP_ID",  # CircleCI
    "ALGOLIA_API_KEY",  # CircleCI
    "CI_COA_PUBLISHER_V2_URL_PR",
    "COA_PUBLISHER_V2_API_KEY_PR",
    "CI_COA_PUBLISHER_V2_URL_STAGING",
    "COA_PUBLISHER_V2_API_KEY_STAGING",
    "CI_COA_PUBLISHER_V2_URL_PROD",
    "COA_PUBLISHER_V2_API_KEY_PROD",
    "SUPERADMIN_USER_PASSWORD",
    "IMPORTER_USER_PASSWORD"
]
for v in vars_from_circleci:
    config[v] = os.getenv(v, "")

# Set additional environment variables not from os
default_branch_vars = {
    "PYTHONUNBUFFERED": 1,
    "WEB_CONCURRENCY": 2,
    "DEBUG": 0,
    "DEBUG_TOOLBAR": False,
    "MONITOR_PERFORMANCE": False,
    "DELETION_PROTECTION": 0,
    "DJANGO_LOG_LEVEL": "INFO",
    "LOAD_DATA": "fixtures",
    "V3_WIP": True,
}
config.update(default_branch_vars)

circle_branch = os.getenv("CIRCLE_BRANCH")
if circle_branch == "pytest":
    config.update({
        'LOAD_DATA': 'test',
    })

# Set any vars for your branch from branch_overrides
branch_override = branch_overrides.get(circle_branch)
if branch_override:
    config.update(branch_override)

# Set your config as your Heroku PR app's environment variables
headers = {
    "Accept": "application/vnd.heroku+json; version=3",
    "Authorization": f"Bearer {os.getenv('HEROKU_API_KEY')}"
}
response = requests.patch(f'https://api.heroku.com/apps/{os.getenv("APPNAME")}/config-vars', headers=headers, data=config)
if response.status_code != 200:
    print(f"{response.status_code} Error: {response.content.decode('utf-8')}")
    sys.exit(1)
else:
    print("Environment variables updated successfully.")
