from django.shortcuts import render
from django.http.request import QueryDict
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from wagtail.core.models import Page
from wagtail.search.query import MATCH_ALL
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.auth import user_has_any_page_permission
# wagtail.admin.auth.user_passes_test does not redirect to settings.LOGIN_URL
# So we must use django.contrib.auth.decorators.user_passes_test
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.vary import vary_on_headers

"""
 Joplin Note:
 - The search method was brought in from wagtail admins views/pages.py file...
 - See referenced file here: https://github.com/wagtail/wagtail/blob/a459e91692659aba04e662978857d14061aecaee/wagtail/admin/views/pages.py#L917
 - Joplin needs more control over our searches in how we sort/filter and display
 the page data the out of the box wagtail provides.
 The main things that we changed from vanilla:
 - we 'run' the query as soon as you visit the page (before any search),
   so we can populate it with summary counts and sort stuff
 - excluding certain pages from the pages to query
"""

@vary_on_headers('X-Requested-With')
@user_passes_test(user_has_any_page_permission)
def search(request):
    # excluding Root(1) and Home(3) pages from search
    pages = all_pages = Page.objects.all().exclude(id__in=[1, 3]).prefetch_related('content_type').specific()
    # blarg = request.user.groups.all()
    user_departments = [user_group for user_group in request.user.groups.all() if hasattr(user_group, 'department')]

    # TODO: use cleaner filtering
    filtered_pages = []
    for page in pages:
        blarg = page.group_permissions.all()
        for bl in blarg:
            if bl.group in user_departments:
                filtered_pages.append(page)
    pages = all_pages = filtered_pages

    q = MATCH_ALL
    content_types = []
    pagination_query_params = QueryDict({}, mutable=True)
    ordering = None

    if 'ordering' in request.GET:
        if request.GET['ordering'] in ['content_type', '-content_type', 'owner', '-owner', 'title', '-title', 'latest_revision_created_at', '-latest_revision_created_at', 'live', '-live']:
            ordering = request.GET['ordering']
            pages = pages.order_by(ordering)

    if 'content_type' in request.GET:
        pagination_query_params['content_type'] = request.GET['content_type']

        app_label, model_name = request.GET['content_type'].split('.')

        try:
            selected_content_type = ContentType.objects.get_by_natural_key(app_label, model_name)
        except ContentType.DoesNotExist:
            raise Http404

        pages = pages.filter(content_type=selected_content_type)
    else:
        selected_content_type = None

    query = ''

    """
     JOPLIN NOTE:
      - Some of this the original state of the query condition has been modified
      because we needed data from the query condition for in our inital display
      on the main content page.
      - For Original code See:
      https://github.com/wagtail/wagtail/blob/a459e91692659aba04e662978857d14061aecaee/wagtail/admin/views/pages.py#L917
    """
    if 'q' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():

            q = form.cleaned_data['q']
            pagination_query_params['q'] = q
            query = q
            pages = pages.search(q)
            """
             - In the original code from wagtail, the content type builder was
             only created for queries. But Joplin wants the contents types for
             the original render of page too.
             - SO, we've moved that outside of this condition. See: "Content Type Builder"
            """

    else:
        form = SearchForm()

    # "Content Type Builder" Joplin Note: Moved from query condition above.
    all_pages = all_pages.search(q, order_by_relevance=not ordering, operator='and')
    content_types = [
        (ContentType.objects.get(id=content_type_id), count)
        for content_type_id, count in all_pages.facet('content_type_id').items()
    ]

    paginator = Paginator(pages, per_page=20)
    pages = paginator.get_page(request.GET.get('p'))

    if request.is_ajax():
        return render(request, "wagtailadmin/pages/search_results.html", {
            'pages': pages,
            'all_pages': all_pages,
            'query_string': query,
            'content_types': content_types,
            'selected_content_type': selected_content_type,
            'ordering': ordering,
            'pagination_query_params': pagination_query_params.urlencode(),
        })
    else:
        return render(request, "wagtailadmin/pages/search.html", {
            'search_form': form,
            'pages': pages,
            'all_pages': all_pages,
            'query_string': query,
            'content_types': content_types,
            'selected_content_type': selected_content_type,
            'ordering': ordering,
            'pagination_query_params': pagination_query_params.urlencode(),
        })
