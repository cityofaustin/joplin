from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from wagtail.core.signals import page_published, page_unpublished

import heroku3
from heroku3.models.build import Build

import boto3

import logging
logger = logging.getLogger(__name__)

JANIS_SLUG_URL = settings.JANIS_SLUG_URL


def create_build_aws(content_type, instance, publish_action='edited', request=None):
    """
        Triggers a build in Amazon Elastic Container Service, it requires:
        1. DEPLOYMENT_MODE
            - The name of the environment in github: production or staging.
            - "PRODUCTION" builds code in the production branch
            - "STAGING"    builds code in the master branch.
        2. AWS_BUCKET_NAME
            - The name of the bucket where the deployment is happening.
            - The bucket name only, not a path.
        3. AWS_CF_DISTRO:
            - The name of the distribution for production.
            - IE: E455RV7LE5UVG
    """
    logger.debug("create_build_aws() Starting task")

    slack_message = ""

    try:
        slack_message = "%s '%s' was %s by user: %s " % (content_type, instance, publish_action, request.user.email)
        print(slack_message)
    except BaseException:
        slack_message = ""

    logger.debug("create_build_aws() Message: " + slack_message)

    if(settings.DEPLOYMENT_MODE in ["PRODUCTION", "STAGING"]):

        # First we initialize our AWS handler (client)
        client = boto3.client(
            'ecs',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        # Now we request to run a container (task) on AWS ECS on Fargate
        response = client.run_task(
            cluster='janis-cluster',
            taskDefinition=settings.AWS_ECS_TASK_DEFINITION,  # ie. 'janis-worker:10'
            launchType='FARGATE',
            count=1,
            platformVersion='LATEST',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': ['subnet-01ab57a13c8e8ab3b'],
                    'assignPublicIp': 'ENABLED',
                    'securityGroups': ['sg-05def9abc5a743581'],
                },
            },
            overrides={
                'containerOverrides': [
                    {
                        'name': 'janis-worker',
                        'environment': [
                            {
                                'name': 'DEPLOYMENT_MODE',
                                'value': settings.DEPLOYMENT_MODE  # 'PRODUCTION' OR 'STAGING'
                            },
                            {
                                'name': 'AWS_BUCKET_NAME',
                                'value': settings.AWS_ECS_DEPLOYMENT_BUCKET  # ie. 'janis-lab'
                            },
                            {
                                'name': 'AWS_CF_DISTRO',
                                'value': settings.AWS_CLOUDFRONT_DISTRIBUTION  # 'E455RV7LE5UVG'
                            },
                            {
                                'name': 'CMS_API',
                                'value': settings.JANIS_CMS_API  # 'https://joplin.herokuapp.com/api/graphql'
                            },
                            {
                                'name': 'CMS_MEDIA',
                                'value': settings.JANIS_CMS_MEDIA  # 'https://joplin-austin-gov-static.s3.amazonaws.com/production/media'
                            },
                            {
                                'name': 'CMS_DOCS',
                                'value': settings.JANIS_CMS_DOCS  # 'https://joplin-austin-gov-static.s3.amazonaws.com/production/media/documents'
                            },
                            {
                                'name': 'SLACK_MESSAGE',
                                'value': slack_message
                            }
                        ]
                    }
                ]
            }
        )
        # We log our response for debugging
        logger.debug(f'Response: {response}')

# Deprecation Notice:
# Since we no longer have Janis builds on Heroku, I don't think this function is needed.
# As a first deprecation step, we will stop requiring HEROKU_JANIS_APP_NAME="janis-staging" as an env variable.
# When coa-publisher is complete for production, we can safely remove this function.
def create_build_if_configured():
    if not all([settings.HEROKU_KEY, settings.HEROKU_JANIS_APP_NAME]):
        logger.warning('Not triggering Janis build because the required settings are not configured.')
        logger.warning(f'HEROKU_KEY={settings.HEROKU_KEY}')
        logger.warning(f'HEROKU_JANIS_APP_NAME={settings.HEROKU_JANIS_APP_NAME}')
        return

    heroku = heroku3.from_key(settings.HEROKU_KEY)
    app = heroku.apps()[settings.HEROKU_JANIS_APP_NAME]

    build = create_build(heroku, app, JANIS_SLUG_URL)
    logger.info(f'Created build {build}')


def create_build(heroku, app, url, checksum=None, version=None, buildpack_urls=None):
    """Create a new release for this app.
       NOTE: Adapted from heroku3.py's create_release
       https://github.com/martyzz1/heroku3.py/blob/8b691c123e039204ad460ae6cf91e98de96a597e/heroku3/models/app.py#L507-L517
    """
    buildpack_urls = buildpack_urls or []
    payload = {
        'source_blob': {
            'url': url,
            'checksum': checksum,
            'version': version,
        },
        'buildpacks': [{'url': buildpack_url} for buildpack_url in buildpack_urls],
    }

    resp = heroku._http_resource(
        method='POST',
        resource=('apps', app.name, 'builds'),
        data=heroku._resource_serialize(payload),
    )
    resp.raise_for_status()

    item = heroku._resource_deserialize(resp.text)
    return Build.new_from_dict(item, h=heroku, app=app)


#
# Returns a Django request object
#

def get_http_request():
    """
        Probably a bad-practice & non-performant approach,
        returns a django request object.
        https://docs.djangoproject.com/en/2.2/ref/request-response/
    """
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            # looking good...
            return frame_record[0].f_locals['request']
            break
    else:
        # looking bad...
        return None
