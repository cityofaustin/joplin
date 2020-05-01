import os
from pages.location_page.fixtures.helpers.create_fixture import create_fixture
import pages.location_page.fixtures.helpers.components as components


# A Live location page sample
def live_library():
    page_data = {
        "imported_revision_id": None,
        "live": True,
        "parent": components.home(),
        "coa_global": False,
        "title": "Faulk Library",
        "slug": "faulk-library",
        "physical_street": "800 Guadalupe St.",
        "physical_zip": 78701,
        "physical_city": "Austin",
        "physical_state": "TX",
    }

    return create_fixture(page_data, os.path.basename(__file__))
