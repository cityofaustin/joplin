from .test_cases.title import title
from .test_cases.at_city_location import at_city_location
from .test_cases.at_remote_location import at_remote_location
from .test_cases.three_fees import three_fees


# You can import any test_case fixture individually
# Or you can load them all with this function
def load_all():
    title()
    at_city_location()
    at_remote_location()
    three_fees()
