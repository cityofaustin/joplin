from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from wagtail.core.models import Page, UserPagePermissionsProxy, GroupPagePermission
from django.core.exceptions import PermissionDenied, ValidationError
from wagtail.admin.views import pages
from wagtail.admin import messages
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.conf import settings
from base.models import Theme
from pages.service_page.models import ServicePage
from pages.information_page.models import InformationPage
from pages.topic_page.models import TopicPage
from pages.topic_collection_page.models import TopicCollectionPage
from pages.topic_collection_page.factories import create_topic_collection_page_from_page_dictionary
from pages.department_page.models import DepartmentPage
from pages.official_documents_page.models import OfficialDocumentPage
from pages.guide_page.models import GuidePage
from pages.form_container.models import FormContainer
from pages.location_page.models import LocationPage
from pages.event_page.models import EventPage
from pages.home_page.models import HomePage
from groups.models import Department
from importer.page_importer import PageImporter
from base.models.site_settings import JanisBranchSettings
from django.contrib.contenttypes.models import ContentType
import json


def import_page_from_url(url):
    page = PageImporter(url).fetch_page_data().create_page()

    return page.id


def new_page_from_modal(request):
    user_perms = UserPagePermissionsProxy(request.user)
    if not user_perms.can_edit_pages():
        raise PermissionDenied

    if request.method == 'POST':
        # Get the page data
        body = json.loads(request.body)
        print(body['type'])

        # if we got an import request, let's go try some importing
        if body['type'] == 'importSinglePage':
            # Respond with the id of the new page
            new_page_id = import_page_from_url(body['title'])
            response = HttpResponse(json.dumps({'id': new_page_id}), content_type="application/json")
            return response

        data = {}
        data['title'] = body['title']
        data['owner'] = request.user

        # Create the page
        if body['type'] == 'service':
            page = ServicePage(**data)
        elif body['type'] == 'information':
            page = InformationPage(**data)
        elif body['type'] == 'topic':
            page = TopicPage(**data)
        elif body['type'] == 'topiccollection':
            if body['theme'] is not None:
                data['theme'] = Theme.objects.get(id=body['theme'])
            page = TopicCollectionPage(**data)
        elif body['type'] == 'department':
            page = DepartmentPage(**data)
        elif body['type'] == 'documents':
            page = OfficialDocumentPage(**data)
        elif body['type'] == 'guide':
            page = GuidePage(**data)
        elif body['type'] == 'form':
            page = FormContainer(**data)
        elif body['type'] == 'location':
            page = LocationPage(**data)
        elif body['type'] == 'event':
            page = EventPage(**data)

        # Add it as a child of home
        home = HomePage.objects.first()
        home.add_child(instance=page)

        # Save our draft
        page.save_revision()
        page.unpublish()  # Not sure why it seems to go live by default

        if request.user.is_superuser:
            # If the user's an admin, add the selected department from
            # the create content modal
            department_id = body['department']
            if department_id:
                department_group = Department.objects.get(pk=department_id)
                GroupPagePermission.objects.create(
                    group=department_group,
                    page=page,
                    permission_type='edit'
                )
        else:
            # If the user's not an admin, then we want to create a
            # group permission object for each of the user's assigned departments
            for user_group in request.user.groups.all():
                # If we did this with non department groups it might cause issues
                if user_group and hasattr(user_group, 'department'):
                    GroupPagePermission.objects.create(
                        group=user_group,
                        page=page,
                        permission_type='edit'
                    )

        # Respond with the id of the new page
        response = HttpResponse(json.dumps({'id': page.id}), content_type="application/json")
        return response
