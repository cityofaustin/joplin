from .test_cases.title import title
from .test_cases.event_with_date import event_with_date


# You can import any test_case fixture individually
# Or you can load them all with this function
def load_all():
    title()
    event_with_date()
