from .test_cases.title import title
from .test_cases.city_location import city_location
from .test_cases.remote_location import remote_location
from .test_cases.three_fees import three_fees


# You can import any test_case fixture individually
# Or you can load them all with this function
def load_all():
    title()
    city_location()
    remote_location()
    three_fees()
