from .test_cases.title import title
from .test_cases.kitchen_sink import kitchen_sink
from groups.fixtures.administrative.group_permissions import add_moderator_permissions, add_editor_permissions
from groups.fixtures.administrative.translators import translators

# You can import any test_case fixture individually
# Or you can load them all with this function
def load_all():
    title()
    kitchen_sink()
