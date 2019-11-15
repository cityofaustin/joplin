from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import (
    Location)


class LocationAdmin(ModelAdmin):
    model = Location
    menu_label = 'Location'  # ditch this to use verbose_primary_name_plural from model
    menu_icon = 'maps'  # change as required
    list_display = ('full_address',)
    list_filter = ('full_address',)
    search_fields = ('full_address',)


modeladmin_register(LocationAdmin)
