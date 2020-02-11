from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from wagtail.core.models import Page, UserPagePermissionsProxy, GroupPagePermission
from django.core.exceptions import PermissionDenied
from wagtail.admin.views import pages
from wagtail.admin import messages
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.conf import settings
from base.models import ServicePage, ProcessPage, InformationPage, TopicPage, TopicCollectionPage, DepartmentPage, Theme, OfficialDocumentPage, GuidePage, FormContainer
from locations.models import LocationPage
from events.models import EventPage
from base.models.site_settings import JanisBranchSettings
from django.contrib.contenttypes.models import ContentType
import json

def new_page_from_modal(request):
    user_perms = UserPagePermissionsProxy(request.user)
    if not user_perms.can_edit_pages():
        raise PermissionDenied

    if request.method == 'POST':
        # Get the page data
        body = json.loads(request.body)
        print(body['type'])
        data = {}
        data['title'] = body['title']
        data['owner'] = request.user

        # Create the page
        if body['type'] == 'service':
            page = ServicePage(**data)
        elif body['type'] == 'process':
            page = ProcessPage(**data)
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
        home = Page.objects.get(id=3)
        home.add_child(instance=page)

        # Save our draft
        page.save_revision()
        page.unpublish()  # Not sure why it seems to go live by default

        # Create a group permission object that allows each of the user's departments to edit this page
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
