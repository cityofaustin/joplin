from .test_cases.title import title
from .test_cases.live_library import live_library
from .test_cases.live_city_hall import live_city_hall


# You can import any test_case fixture individually
# Or you can load them all with this function
def load_all():
    title()
    live_library()
    live_city_hall()
