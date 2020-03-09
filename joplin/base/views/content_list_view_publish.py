# DEPRECATED
# This was the code we used to publish pages from the home Content List View.
# We no longer do this because it is not compatible with PublishRequirements.
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from wagtail.core.models import Page, UserPagePermissionsProxy
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

# This method is used on the home Pages page.
# When you want to publish a page directly from the home page, this route is called.
# The publish button on the edit/ page sends a "action-publish" message directly to wagtail.
# "action-publish" does not use this endpoint.


def publish(request, page_id):
    # We'll get a weird MetaClass for our page.base_form_class if we don't use page.specific
    page = get_object_or_404(Page, id=page_id).specific

    user_perms = UserPagePermissionsProxy(request.user)
    if not user_perms.for_page(page).can_publish():
        raise PermissionDenied

    next_url = pages.get_valid_next_url_from_request(request)

    if request.method == 'POST':
        # Check Publish Requirements, redirect to edit page if any requirements are unmet
        if hasattr(page, "publish_requirements"):
            publish_requirements = page.publish_requirements
            unmet_criteria = page.base_form_class.check_publish_requirements(
                publish_requirements,
                json.loads(page.to_json())
            )
            if unmet_criteria:
                messages.error(request, _("Page '{0}' has unmet publishing requirements.").format(page.get_admin_display_title()))
                return redirect(f'/admin/pages/{page.id}/edit/')

        # Publish the latest revision
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
        return redirect('/admin/pages/search/')

    return render(request, 'wagtailadmin/pages/confirm_publish.html', {
        'page': page,
        'next': next_url,
    })


# This was the url added to urls.py
url = url(r'admin/pages/(\d+)/publish/$', joplin_views.publish, name='publish')

# This was the logic added to @hooks.register('register_joplin_page_listing_more_buttons')
# in order to add a "Publish" option to the Content List View's "more" dropdown
# if page_perms.can_publish() and page.has_unpublished_changes:
#     yield Button(
#         _('Publish'),
#         reverse('publish', args=[page.id]),
#         attrs={'title': _("Publish page '{title}'").format(
#             title=page.get_admin_display_title())},
#         priority=50
#     )
