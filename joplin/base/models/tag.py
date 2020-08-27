from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TagBase, ItemBase
from wagtail.snippets.models import register_snippet


@register_snippet
class PageTag(TagBase):
    '''
    With a custom "Tag" class, we can extend Tags to include other attributes, like a related department.

    By default, tag fields work on a “free tagging” basis: editors can enter anything into the field,
    and upon saving, any tag text not recognised as an existing tag will be created automatically.
    We disable this functionality with `free_tagging = False`
    '''
    free_tagging = False


class TaggedPage(ItemBase):
    '''
    https://docs.wagtail.io/en/v2.10.1/reference/pages/model_recipes.html#custom-tag-models
    '''
    tag = models.ForeignKey(
        PageTag, related_name="tagged_page", on_delete=models.CASCADE
    )
    content_object = ParentalKey(
        to='base_page.JanisBasePage',
        on_delete=models.CASCADE,
        related_name='page_tags'
    )
