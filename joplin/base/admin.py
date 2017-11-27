from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from base.models import Event, Department


class EventModelAdmin(ModelAdmin):
    model = Event


class DepartmentModelAdmin(ModelAdmin):
    model = Department


class ReallyAwesomeGroup(ModelAdminGroup):
    menu_label = 'Awesome things'
    items = (EventModelAdmin, DepartmentModelAdmin)


modeladmin_register(ReallyAwesomeGroup)
