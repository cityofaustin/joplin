from .test_cases.title import title
from .test_cases.live import live


# You can import any test_case fixture individually
# Or you can load them all with this function
def load_all():
    title()
    live()
