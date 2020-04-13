from snippets.theme.models import Theme
from factory import DjangoModelFactory


class ThemeFactory(DjangoModelFactory):
    class Meta:
        model = Theme
