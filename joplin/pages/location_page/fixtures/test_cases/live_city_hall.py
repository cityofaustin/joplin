import os
from pages.location_page.fixtures.helpers.create_fixture import create_fixture
import pages.location_page.fixtures.helpers.components as components
import pages.service_page.fixtures as service_page_fixtures


# A Live location page sample
def live_city_hall():
    service_page = service_page_fixtures.title()
    related_services = [{
        "related_service": service_page,
        **components.location_hours()
    }]

    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "City Hall",
        "slug": "city-hall",
        "physical_street": "124 West 8th St.",
        "physical_zip": 78701,
        "physical_city": "Austin",
        "physical_state": "TX",
        **components.location_hours(),
        "add_related_services": related_services
    }

    return create_fixture(page_data, os.path.basename(__file__))
