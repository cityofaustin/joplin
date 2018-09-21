from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from wagtail.core.models import Page, UserPagePermissionsProxy
from wagtail.admin.views import pages
from wagtail.admin import messages
from django.utils.translation import ugettext as _
from django.urls import reverse

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

    # TODO: check permissions for making pages
    # if not user_perms.for_page(page).can_publish():
    #     raise PermissionDenied

    # TODO: Redirects
    # next_url = pages.get_valid_next_url_from_request(request)

    if request.method == 'POST':
        print(request)
        response = HttpResponse("Text only, please.", content_type="text/plain")
        return response
        # page.get_latest_revision().publish()

        # TODO: messages maybe
        # messages.success(request, _("Page '{0}' published.").format(page.get_admin_display_title()), buttons=[
        #     messages.button(reverse('wagtailadmin_pages:edit', args=(page.id,)), _('Edit'))
        # ])

        # TODO: Redirects
        # if next_url:
        #     return redirect(next_url)