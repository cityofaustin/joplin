from django.urls import path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from base.views import joplin_views

from base.models import HomePage


def home(request):
    page = HomePage.objects.first()
    return redirect('wagtailadmin_explore', page.id)


urlpatterns = [
    url(r'^django-admin/', include('smuggler.urls')),
    url(r'^django-admin/', admin.site.urls),

    path('admin/', home),
    url(r'admin/pages/(\d+)/publish/$', joplin_views.publish, name='publish'),
    url(r'admin/pages/new_from_modal/$', joplin_views.new_page_from_modal, name='new_page_from_modal'),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^api/graphql', csrf_exempt(GraphQLView.as_view())),
    url(r'^api/graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True, pretty=True))),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
