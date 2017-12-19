from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html, format_html_join

from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.wagtailcore import hooks

from base.models import ApplicationBlock, Topic, Location, Contact


@hooks.register('insert_editor_css')
def editor_css():
    urls = [
        static('css/admin.css'),
        static('css/toggle.css'),
        static('css/preview.css'),
    ]
    return format_html_join('\n', '<link rel="stylesheet" href="{}">', ((url,) for url in urls))


@hooks.register('insert_editor_js')
def editor_js():
    urls = [
        'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.4/lodash.min.js',
        static('js/admin.js'),
    ]
    return format_html_join('\n', '<script src="{}"></script>', ((url,) for url in urls))


@hooks.register('before_edit_page')
def before_edit_page(request, page):
    print(f'BeforeEditHook request: {request}')
    print(f'BeforeEditHook page: "{page}" of type "{type(page)}"')

    assert request.user.is_authenticated()
    print(f'BeforeEditHook {request.user.email} is in groups {[group.name for group in request.user.groups.all()]}')


class ApplicationBlockModelAdmin(ModelAdmin):
    model = ApplicationBlock


class LocationModelAdmin(ModelAdmin):
    model = Location
    search_fields = ('street',)


class TopicModelAdmin(ModelAdmin):
    model = Topic
    search_fields = ('text',)


class ContactModelAdmin(ModelAdmin):
    model = Contact


class ReallyAwesomeGroup(ModelAdminGroup):
    menu_label = 'Awesome Things'
    items = (ApplicationBlockModelAdmin, LocationModelAdmin, TopicModelAdmin, ContactModelAdmin)


modeladmin_register(ReallyAwesomeGroup)
