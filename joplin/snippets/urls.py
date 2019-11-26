from django.conf.urls import url

from wagtail.snippets.views import chooser, snippets
from base.views import snippets as joplin_snippets

# use our version of the edit view, wagtail defaults for the rest

app_name = 'joplinsnippets'
urlpatterns = [
    url(r'^$', snippets.index, name='index'),

    url(r'^choose/$', chooser.choose, name='choose_generic'),
    url(r'^choose/(\w+)/(\w+)/$', chooser.choose, name='choose'),
    url(r'^choose/(\w+)/(\w+)/([^/]+?)/$', chooser.chosen, name='chosen'),

    url(r'^(\w+)/(\w+)/$', snippets.list, name='list'),
    url(r'^(\w+)/(\w+)/add/$', snippets.create, name='add'),
    url(r'^(\w+)/(\w+)/([^/]+?)/$', joplin_snippets.edit, name='edit'),
    url(r'^(\w+)/(\w+)/multiple/delete/$', snippets.delete, name='delete-multiple'),
    url(r'^(\w+)/(\w+)/([^/]+?)/delete/$', snippets.delete, name='delete'),
    url(r'^(\w+)/(\w+)/([^/]+?)/usage/$', snippets.usage, name='usage'),
]
