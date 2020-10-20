import sys
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.utils import translation

from pages.base_page.models import JanisBasePage
from pages.official_documents_page.models import OfficialDocumentPage

@api_view(['GET'])
def site_search(request):
    try:
        params = request.query_params
        q = (params.get("q") or "")[:100] # only allow 100 characters max
        page = int(params.get("page") or 1)
        limit = int(params.get("limit") or 10)
        lang = params.get("lang") or "en"
        official_document_collection_id = params.get("official_document_collection_id")
        result = None

        # A query for an official_document_collection will only need to return the pages that are part of it.
        if (official_document_collection_id):
            '''
            We can't run on .search() on a .filter() that filters by a foreign key. This is a limitation in Wagtail https://docs.wagtail.io/en/v2.10.2/topics/search/indexing.html#index-relatedfields
            But there's a workaround. You can run one query that just gets all the ids you want.
            Then run a search on that QuerySet.
            This is the workaround recommended by Wagtail "as long as you don't have 1000s of pages" https://groups.google.com/g/wagtail/c/k2-E4h2oLtI/m/uPOzbuwKBgAJ
            '''
            doc_ids_for_collection = OfficialDocumentPage.objects.filter(
                published=True, live=True,
                official_document_collection__official_document_collection__id__in=[official_document_collection_id]
            ).values_list('id', flat=True)

            result = OfficialDocumentPage.objects.filter(
                id__in=doc_ids_for_collection
            ).order_by("-date").search(q)
        # If a query doesn't have an official_document_collection_id, then assume that it's for the global SearchPage
        else:
            result = JanisBasePage.objects.filter(published=True, live=True).search(q)

        offset = ((page-1) * limit)
        result = result[offset:(offset + limit)]

        # Set the set language for return values
        translation.activate(lang)
        # return HttpResponse([r.to_json() for r in result], content_type='application/json')
        return HttpResponse([r.specific.search_output for r in result], content_type="application/json")
    except Exception as err:
        print(f"Error on site_search", sys.exc_info()[0])
        return HttpResponse(500)