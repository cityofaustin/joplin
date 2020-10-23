import sys
import math
import json
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.utils import translation

from pages.base_page.models import JanisBasePage
from pages.official_documents_page.models import OfficialDocumentPage

'''
    ex:
        http://localhost:8000/site_search?q=get&page=3&limit=20&lang=es
        http://localhost:8000/site_search?lang=en&limit=10&officialDocumentCollectionId=319&page=1
'''
@api_view(['GET'])
def site_search(request):
    try:
        params = request.query_params
        q = (params.get("q") or "")[:100] # only allow 100 characters max
        page = int(params.get("page") or 1)
        limit = int(params.get("limit") or 10)
        lang = params.get("lang") or "en"
        to_date = params.get("toDate")
        from_date = params.get("fromDate")
        official_document_collection_id = params.get("officialDocumentCollectionId")
        result_data = []
        result_meta = {}

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

            filter = {
                "id__in": doc_ids_for_collection,
            }
            if to_date:
                filter["date__lte"] = to_date
            if from_date:
                filter["date__gte"] = from_date

            result_data = OfficialDocumentPage.objects.filter(
                **filter
            ).order_by("-date")

            # q is not mandatory for searching in OfficialDocumentCollection
            if q:
                result_data = result_data.search(q)

        # If a query doesn't have an official_document_collection_id, then assume that it's for the global SearchPage
        else:
            result_data = JanisBasePage.objects.filter(published=True, live=True).search(q)

        result_meta["totalResults"] = result_data.count()
        result_meta["totalPages"] = math.ceil(result_meta["totalResults"]/limit)
        offset = ((page-1) * limit)
        result_data = result_data[offset:(offset + limit)]

        # Set the language for search_output values
        translation.activate(lang)
        result_data = [r.specific.search_output for r in result_data]

        return HttpResponse(json.dumps({
            "_meta": result_meta,
            "data": result_data,
        }), content_type="application/json")
    except Exception as err:
        print(f"Error on site_search", sys.exc_info())
        return HttpResponse(status=500)
