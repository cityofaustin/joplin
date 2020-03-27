from .test_cases.title import title
from .test_cases.steps_2 import steps_2
from .test_cases.steps_with_appblocks import steps_with_appblocks
from .test_cases.new_contact import new_contact


# You can import any test_case fixture individually
# Or you can load them all with this function
def load_all():
    title()
    steps_2()
    steps_with_appblocks()
    new_contact()
