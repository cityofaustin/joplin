from pages.home_page.fixtures import root_home_page
from groups.fixtures import add_moderator_permissions, add_editor_permissions, translators


# Run the fixtures required for Joplin to run.
def load_all():
    root_home_page()
    add_moderator_permissions()
    add_editor_permissions()
    translators()
