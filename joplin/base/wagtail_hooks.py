from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html, format_html_join

from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.wagtailcore import hooks

from base.models import ApplicationBlock, Event, Department


@hooks.register('insert_editor_css')
def editor_css():
    urls = [
        static('css/admin.css'),
        static('css/toggle.css'),
    ]
    return format_html_join('\n', '<link rel="stylesheet" href="{}">', ((url,) for url in urls))


@hooks.register('insert_editor_js')
def editor_js():
    return format_html('<script src="{}">', static('js/admin.js'))


@hooks.register('before_edit_page')
def before_edit_page(request, page):
    print(f'BeforeEditHook request: {request}')
    print(f'BeforeEditHook page: "{page}" of type "{type(page)}"')

    assert request.user.is_authenticated()
    print(f'BeforeEditHook {request.user.email} is in groups {[group.name for group in request.user.groups.all()]}')


class ApplicationBlockModelAdmin(ModelAdmin):
    model = ApplicationBlock


class EventModelAdmin(ModelAdmin):
    model = Event


class DepartmentModelAdmin(ModelAdmin):
    model = Department
    list_display = ('name', 'address')
    search_fields = ('name',)


class ReallyAwesomeGroup(ModelAdminGroup):
    menu_label = 'Awesome Things'
    items = (ApplicationBlockModelAdmin, EventModelAdmin, DepartmentModelAdmin)


modeladmin_register(ReallyAwesomeGroup)
