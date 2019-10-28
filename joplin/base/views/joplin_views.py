from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.http.request import QueryDict
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from wagtail.core.models import Page, UserPagePermissionsProxy
from wagtail.admin.views import pages
from wagtail.admin import messages
from wagtail.search.query import MATCH_ALL
from wagtail.admin.forms.search import SearchForm
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.conf import settings
from base.models import ServicePage, ProcessPage, InformationPage, TopicPage, TopicCollectionPage, DepartmentPage, Theme, OfficialDocumentPage, GuidePage
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
        if body['type'] == 'process':
            page = ProcessPage(**data)
        if body['type'] == 'information':
            page = InformationPage(**data)
        if body['type'] == 'topic':
            page = TopicPage(**data)
        if body['type'] == 'topiccollection':
            if body['theme'] is not None:
                data['theme'] = Theme.objects.get(id=body['theme'])
            page = TopicCollectionPage(**data)
        if body['type'] == 'department':
            page = DepartmentPage(**data)
        if body['type'] == 'documents':
            page = OfficialDocumentPage(**data)
        if body['type'] == 'guide':
            page = GuidePage(**data)

        # Add it as a child of home
        home = Page.objects.get(id=3)
        home.add_child(instance=page)

        # Save our draft
        page.save_revision()
        page.unpublish()  # Not sure why it seems to go live by default

        # Respond with the id of the new page
        response = HttpResponse(json.dumps({'id': page.id}), content_type="application/json")
        return response

# def search(request):
#     pages = all_pages = Page.objects.all().prefetch_related('content_type').specific()
#     q = MATCH_ALL
#     content_types = []
#     pagination_query_params = QueryDict({}, mutable=True)
#     ordering = None
#
#     if 'ordering' in request.GET:
#         if request.GET['ordering'] in ['content_type', '-content_type', 'owner', '-owner', 'title', '-title', 'latest_revision_created_at', '-latest_revision_created_at', 'live', '-live']:
#             ordering = request.GET['ordering']
#
#             # The content_type order column was added so Joplin search results could order alphabetically by content_type
#             if ordering == 'content_type':
#                 pages = pages.order_by('content_type')
#             elif ordering == '-content_type':
#                 pages = pages.order_by('-content_type')
#
#             # The owner order column was added so Joplin search results could order alphabetically by owner
#             if ordering == 'owner':
#                 pages = pages.order_by('owner')
#             elif ordering == '-owner':
#                 pages = pages.order_by('-owner')
#
#             if ordering == 'title':
#                 pages = pages.order_by('title')
#             elif ordering == '-title':
#                 pages = pages.order_by('-title')
#
#             if ordering == 'latest_revision_created_at':
#                 pages = pages.order_by('latest_revision_created_at')
#             elif ordering == '-latest_revision_created_at':
#                 pages = pages.order_by('-latest_revision_created_at')
#
#             if ordering == 'live':
#                 pages = pages.order_by('live')
#             elif ordering == '-live':
#                 pages = pages.order_by('-live')
#
#     if 'content_type' in request.GET:
#         pagination_query_params['content_type'] = request.GET['content_type']
#
#         app_label, model_name = request.GET['content_type'].split('.')
#
#         try:
#             selected_content_type = ContentType.objects.get_by_natural_key(app_label, model_name)
#         except ContentType.DoesNotExist:
#             raise Http404
#
#         pages = pages.filter(content_type=selected_content_type)
#     else:
#         selected_content_type = None
#
#     query = ''
#
#     # JOPLIN NOTE: Some of this the original state of the query condition
#     # has been modified because we needed data of the query condition
#     # for in our inital display on the main content page.
#     # For Original Code > See: https://github.com/wagtail/wagtail/blob/a459e91692659aba04e662978857d14061aecaee/wagtail/admin/views/pages.py#L917
#     if 'q' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#
#             q = form.cleaned_data['q']
#             pagination_query_params['q'] = q
#             query = q
#             pages = pages.search(q)
#             # In the original code from wagtail, the content type builder was only created for queries.
#             # But Joplin wants the contents types for the original render of page too
#             # SO, we've moved outside of the condition below:
#             # See: "Content Type Builder"
#
#     else:
#         form = SearchForm()
#         # JOPLIN NOTE: This is where we "hide" the home and root page on initial load of main content page.
#         # - However, these pages will be available in any search that matches title.
#         for page in pages:
#             if page.title == "Root" or page.title == "Home":
#                 pages = pages.not_page(page)
#                 all_pages = all_pages.not_page(page)
#
#     # "Content Type Builder" Joplin Note: Moved from query condition above.
#     all_pages = all_pages.search(q, order_by_relevance=not ordering, operator='and')
#     content_types = [
#         (ContentType.objects.get(id=content_type_id), count)
#         for content_type_id, count in all_pages.facet('content_type_id').items()
#     ]
#
#     paginator = Paginator(pages, per_page=20)
#     pages = paginator.get_page(request.GET.get('p'))
#
#     if request.is_ajax():
#         return render(request, "wagtailadmin/pages/search_results.html", {
#             'pages': pages,
#             'all_pages': all_pages,
#             'query_string': q,
#             'content_types': content_types,
#             'selected_content_type': selected_content_type,
#             'ordering': ordering,
#             'pagination_query_params': pagination_query_params.urlencode(),
#         })
#     else:
#         return render(request, "wagtailadmin/pages/search.html", {
#             'search_form': form,
#             'pages': pages,
#             'all_pages': all_pages,
#             'query_string': query,
#             'content_types': content_types,
#             'selected_content_type': selected_content_type,
#             'ordering': ordering,
#             'pagination_query_params': pagination_query_params.urlencode(),
#         })
