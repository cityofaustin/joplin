from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from generic_chooser.views import ModelChooserViewSet

from locations.models import Location


class LocationChooserViewSet(ModelChooserViewSet):
    icon = 'user'
    model = Location
    page_title = _("Choose a location")
    per_page = 10
    order_by = 'full_address'
    fields = ['full_address', 'unit_number', 'geography']
