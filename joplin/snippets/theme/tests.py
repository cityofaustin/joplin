import pytest

from snippets.theme.models import Theme
import snippets.contact.fixtures as fixtures


@pytest.mark.django_db
def test_kitchen_sink():
    theme = fixtures.kitchen_sink()
    assert isinstance(theme, Theme)
    assert theme.text == "Kitchen sink theme [en]"
    assert theme.text_es == "Kitchen sink theme [es]"

