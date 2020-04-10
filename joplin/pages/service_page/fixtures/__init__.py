from .test_cases.title import title
from .test_cases.steps_2 import steps_2
from .test_cases.steps_with_appblocks import steps_with_appblocks
from .test_cases.new_contact import new_contact
from .test_cases.kitchen_sink import kitchen_sink
from .test_cases.steps_2_live import steps_2_live
from .test_cases.steps_with_appblocks_live import steps_with_appblocks_live



# You can import any test_case fixture individually
# Or you can load them all with this function
def load_all():
    title()
    steps_2()
    steps_with_appblocks()
    new_contact()
    kitchen_sink()
    steps_2_live()
    steps_with_appblocks_live()
