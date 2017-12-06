from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html

from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.wagtailcore import hooks

from base.models import ApplicationBlock, Event, Department


@hooks.register('insert_editor_css')
def editor_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/admin.css'))


@hooks.register('insert_editor_js')
def editor_js():
    return format_html('<script src="{}">', static('js/admin.js'))


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
