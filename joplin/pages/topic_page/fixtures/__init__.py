from .test_cases.kitchen_sink import kitchen_sink
from .test_cases.title import title


# You can import any test_case fixture individually
# Or you can load them all with this function
def load_all():
    kitchen_sink()
    title()
