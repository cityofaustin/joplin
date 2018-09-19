from django.shortcuts import get_object_or_404, render
from wagtail.core.models import Page, UserPagePermissionsProxy
from wagtail.admin.views import pages

def publish(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific

    user_perms = UserPagePermissionsProxy(request.user)
    if not user_perms.for_page(page).can_publish():
        raise PermissionDenied

    next_url = pages.get_valid_next_url_from_request(request)

    if request.method == 'POST':

        page.publish()

        messages.success(request, _("Page '{0}' published.").format(page.get_admin_display_title()), buttons=[
            messages.button(reverse('wagtailadmin_pages:edit', args=(page.id,)), _('Edit'))
        ])

        if next_url:
            return redirect(next_url)
        return redirect('wagtailadmin_explore', page.get_parent().id)

    return render(request, 'wagtailadmin/pages/confirm_publish.html', {
        'page': page,
        'next': next_url,
        'live_descendant_count': page.get_descendants().live().count(),
    })