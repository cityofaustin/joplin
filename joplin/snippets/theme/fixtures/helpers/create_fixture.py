from snippets.theme.models import Theme
from snippets.theme.factories import ThemeFactory

# Skips creating fixture if Theme with slug already exists
def create_fixture(theme_data, fixture_name):
    try:
        theme = Theme.objects.get(slug=theme_data['slug'])
    except Theme.DoesNotExist:
        theme = None
    if theme:
        print(f"Skipping {fixture_name}")
        return None

    theme = ThemeFactory.create(**theme_data)
    print(f"Built {fixture_name}")
    return theme
