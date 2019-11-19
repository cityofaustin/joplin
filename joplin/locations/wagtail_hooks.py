from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import (
    Location,
    LocationPage,
    LocationsIndexPage
)
from wagtail.core import hooks

from locations.views import LocationChooserViewSet


class LocationAdmin(ModelAdmin):
    model = Location

    menu_icon = 'maps'  # change as required
    list_display = ('full_address',)
    list_filter = ('full_address',)
    search_fields = ('full_address',)


class LocationPageAdmin(ModelAdmin):
    model = LocationPage

    menu_icon = 'maps'  # change as required
    list_display = ('primary_name', 'physical_address')
    list_filter = ('primary_name', 'physical_address')
    search_fields = ('primary_name', 'physical_address')


class LocationsIndexPageAdmin(ModelAdmin):
    model = LocationsIndexPage
    menu_icon = 'maps'  # change as required


modeladmin_register(LocationAdmin)
modeladmin_register(LocationPageAdmin)
modeladmin_register(LocationsIndexPageAdmin)


@hooks.register('register_admin_viewset')
def register_location_chooser_viewset():
    return LocationChooserViewSet('location_chooser', url_prefix='location-chooser')
