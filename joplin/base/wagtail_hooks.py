from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from django.utils.html import format_html_join

from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.core import hooks

from base.models import HomePage, Topic, Location, Contact

@hooks.register('before_edit_page')
def before_edit_page(request, page):
    print(f'BeforeEditHook request: {request}')
    print(f'BeforeEditHook page: "{page}" of type "{type(page)}"')

    assert request.user.is_authenticated
    print(f'BeforeEditHook {request.user.email} is in groups {[group.name for group in request.user.groups.all()]}')


@hooks.register('construct_main_menu')
def configure_main_menu(request, menu_items):
    new_items = []
    for item in menu_items:
        if item.name in ('home', 'images'):
            item.label = ''
            new_items.append(item)
    menu_items[:] = new_items


@hooks.register('register_admin_menu_item')
def register_page_list_menu_item():
    home = HomePage.objects.first()
    return MenuItem('Home', reverse('wagtailadmin_explore', args=[home.pk]), classnames='icon icon-home', order=10)


class LocationModelAdmin(ModelAdmin):
    model = Location
    search_fields = ('street',)


class TopicModelAdmin(ModelAdmin):
    model = Topic
    search_fields = ('text',)


class ContactModelAdmin(ModelAdmin):
    model = Contact


class ReallyAwesomeGroup(ModelAdminGroup):
    menu_label = 'Important Snippets'
    items = (LocationModelAdmin, TopicModelAdmin, ContactModelAdmin)


modeladmin_register(ReallyAwesomeGroup)
