from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from wagtail.core.models import Page, UserPagePermissionsProxy
from django.core.exceptions import PermissionDenied
from wagtail.admin.views import pages
from wagtail.admin import messages
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.conf import settings
from base.models import ServicePage, ProcessPage, InformationPage, TopicPage, TopicCollectionPage, DepartmentPage, Theme, OfficialDocumentPage, GuidePage, FormPage
from base.models.site_settings import JanisBranchSettings
import json

# This method is used on the home Pages page.
# When you want to publish a page directly from the home page, this route is called.
# The publish button on the edit/ page sends a "action-publish" message directly to wagtail.
# "action-publish" does not use this endpoint.
def publish(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific

    user_perms = UserPagePermissionsProxy(request.user)
    if not user_perms.for_page(page).can_publish():
        raise PermissionDenied

    next_url = pages.get_valid_next_url_from_request(request)

    if request.method == 'POST':

        page.get_latest_revision().publish()

        # TODO: clean up copypasta when coa-publisher phases out previously AWS publish pipeline
        # Show success message if there is a publish_janis_branch set (for netlify builds)
        # Or default to show success message on Staging and Production (follow existing AWS implementation pattern)
        try:
            publish_janis_branch = getattr(JanisBranchSettings.objects.first(), 'publish_janis_branch')
        except:
            publish_janis_branch = None
        if settings.ISSTAGING or settings.ISPRODUCTION:
            messages.success(request, _("Page '{0}' published.").format(page.get_admin_display_title()), buttons=[
                messages.button(reverse('wagtailadmin_pages:edit', args=(page.id,)), _('Edit'))
            ])
        elif settings.ISLOCAL:
            messages.warning(request, _("Page '{0}' not published. You're running on a local environment.").format(page.get_admin_display_title()), buttons=[
                messages.button(reverse('wagtailadmin_pages:edit', args=(page.id,)), _('Edit'))
            ])
        elif publish_janis_branch:
            messages.success(request, _("Page '{0}' published.").format(page.get_admin_display_title()), buttons=[
                messages.button(reverse('wagtailadmin_pages:edit', args=(page.id,)), _('Edit'))
            ])
        else:
            messages.warning(request, _("Page '{0}' not published. No `publish_janis_branch` was set.").format(page.get_admin_display_title()), buttons=[
                messages.button(reverse('wagtailadmin_pages:edit', args=(page.id,)), _('Edit'))
            ])

        if next_url:
            return redirect(next_url)
        # return redirect('wagtailadmin_explore', page.get_parent().id)
        return redirect('pages/search/')


    return render(request, 'wagtailadmin/pages/confirm_publish.html', {
        'page': page,
        'next': next_url,
    })


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
            page = FormPage(**data)

        # Add it as a child of home
        home = Page.objects.get(id=3)
        home.add_child(instance=page)

        # Save our draft
        page.save_revision()
        page.unpublish()  # Not sure why it seems to go live by default

        # Respond with the id of the new page
        response = HttpResponse(json.dumps({'id': page.id}), content_type="application/json")
        return response
