from pages.home_page.fixtures import root_home_page
from groups.fixtures.helpers import group_permissions


# Run the fixtures required for Joplin to run.
def load_all():
    root_home_page()
    group_permissions.add_moderator_permissions()
    group_permissions.add_editor_permissions()

