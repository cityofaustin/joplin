from django.shortcuts import render
from django.http.request import QueryDict
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from wagtail.core.models import Page
from wagtail.search.query import MATCH_ALL
from wagtail.admin.forms.search import SearchForm

"""
 Joplin Note:
 - The search method was brought in from wagtail admins views/pages.py file...
 - See referenced file here: https://github.com/wagtail/wagtail/blob/a459e91692659aba04e662978857d14061aecaee/wagtail/admin/views/pages.py#L917
 - Joplin needs more control over our searches in how we sort/filter and display
 the page data the out of the box wagtail provides.
"""


def search(request):
    pages = all_pages = Page.objects.all().prefetch_related('content_type').specific()
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
        """
          JOPLIN NOTE:
          - This is where we 'hide' the 'home' and 'root' page on initial load of main content page.
          - However, these pages will be available in any search that matches title.
        """
        for page in pages:
            if page.title == "Root" or page.title == "Home":
                pages = pages.not_page(page)
                all_pages = all_pages.not_page(page)

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
            'query_string': q,
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
