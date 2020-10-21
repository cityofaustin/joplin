from pages.home_page.fixtures import root_home_page
from groups.fixtures import add_moderator_permissions, add_editor_permissions, translators
from users.fixtures import user_for_build_process


# Run the fixtures required for Joplin to run.
def load_all():
    root_home_page()
    add_moderator_permissions()
    add_editor_permissions()
    translators()
    user_for_build_process()
