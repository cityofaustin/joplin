from django.conf.urls import url

from users.views import users

app_name = 'joplinusers_users'
urlpatterns = [
    url(r'^$', users.index, name='index'),
    url(r'^add/$', users.create, name='add'),
    url(r'^([^\/]+)/$', users.edit, name='edit'),
    url(r'^([^\/]+)/delete/$', users.delete, name='delete'),
]
