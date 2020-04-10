from snippets.theme.models import Theme
from snippets.theme.factories import ThemeFactory


# Skips creating fixture if theme with the same text already exists
def create_fixture(theme_data, fixture_name):
    try:
        theme = Theme.objects.get(text=theme_data['text'])
    except Theme.DoesNotExist:
        theme = None
    if theme:
        print(f"Skipping theme fixture: {fixture_name}")
        return theme

    theme = ThemeFactory.create(**theme_data)
    print(f"Built theme fixture: {fixture_name}")
    return theme
