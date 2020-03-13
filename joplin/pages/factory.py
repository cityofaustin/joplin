import factory
import wagtail_factories
from django.utils.text import slugify
from wagtail.core.models import Page

# put factories here that can be used in more than one part of the code-base


class PageFactory(wagtail_factories.factories.MP_NodeFactory):
    """
    little hack from wagtail_factories cause I don't want a hard-coded page title
    note: when creating pages give it a parent (parent=<another page like home page>)
    or else it'l be an orphan and you'll both be sad
    """
    title = factory.Faker('first_name')
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))

    class Meta:
        model = Page
