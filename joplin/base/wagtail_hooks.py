from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from base.models import ApplicationBlock, Event, Department


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
