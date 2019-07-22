from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from wagtail.core.models import Page, UserPagePermissionsProxy
from wagtail.admin.views import pages
from wagtail.admin import messages
from django.utils.translation import ugettext as _
from django.urls import reverse
from base.models import ServicePage, ProcessPage, InformationPage, TopicPage, TopicCollectionPage, DepartmentPage, Theme
import json

def publish(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific

    user_perms = UserPagePermissionsProxy(request.user)
    if not user_perms.for_page(page).can_publish():
        raise PermissionDenied

    next_url = pages.get_valid_next_url_from_request(request)

    if request.method == 'POST':

        page.get_latest_revision().publish()

        messages.success(request, _("Page '{0}' published.").format(page.get_admin_display_title()), buttons=[
            messages.button(reverse('wagtailadmin_pages:edit', args=(page.id,)), _('Edit'))
        ])

        if next_url:
            return redirect(next_url)
        return redirect('wagtailadmin_explore', page.get_parent().id)

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
        if body['type'] != 'department' and body['type'] != 'topic':
            if body['department'] != None:
                data['department'] = DepartmentPage.objects.get(id=body['department'])
        data['title'] = body['title']
        data['owner'] = request.user

        # Create the page
        if body['type'] == 'service':
            page = ServicePage(**data)
        if body['type'] == 'process':
            page = ProcessPage(**data)
        if body['type'] == 'information':
            page = InformationPage(**data)
        if body['type'] == 'topic':
            page = TopicPage(**data)
        if body['type'] == 'topiccollection':
            if body['theme'] != None:
                data['theme'] = Theme.objects.get(id=body['theme'])
            page = TopicCollectionPage(**data)
        if body['type'] == 'department':
            data['what_we_do'] = 'What we do'
            data['mission'] = 'Mission'
            page = DepartmentPage(**data)

        # Add it as a child of home
        home = Page.objects.get(id=3)
        home.add_child(instance=page)

        # Save our draft
        page.save_revision()
        page.unpublish() # Not sure why it seems to go live by default

        # Respond with the id of the new page
        response = HttpResponse(json.dumps({'id': page.id}), content_type="application/json")
        return response
