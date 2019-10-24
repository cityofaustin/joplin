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
from django.urls import reverse
# from base.models import HomePage
import debug_toolbar


def home(request):
    # page = HomePage.objects.first()
    print('\n😬😬\n')
    print(request)
    # print(HomePage)
    # print(page, page.id)
    print('\n😬\n')
    # return redirect('wagtailadmin_explore', page.id)
    return redirect('pages/search/')




def login(request):
    return redirect(reverse('wagtailadmin_login'), permanent=True)


urlpatterns = [
    url(r'^django-admin/', include('smuggler.urls')),
    url(r'^django-admin/', admin.site.urls),
    path('admin/docs/', include('django.contrib.admindocs.urls')),
    # uncomment this path to expiriment with the default dashboard,
    # which can be customized using wagtail hooks
    path('admin/', home),
    path('', login),
    url(r'admin/pages/(\d+)/publish/$', joplin_views.publish, name='publish'),
    url(r'admin/pages/new_from_modal/$',
        joplin_views.new_page_from_modal, name='new_page_from_modal'),
    # 🔥
    url(r'admin/pages/search/$', joplin_views.search, name='search'),
    # 🔥
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    path('__debug__/', include(debug_toolbar.urls)),
    url(r'^api/graphql', csrf_exempt(GraphQLView.as_view())),
    url(r'^api/graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True, pretty=True))),
    url(r'session_security/', include('session_security.urls')),


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
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
