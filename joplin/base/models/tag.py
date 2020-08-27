from django.db import models
from modelcluster.models import ClusterableModel
from taggit.models import TagBase, ItemBase
from wagtail.snippets.models import register_snippet


@register_snippet
class PageTag(ClusterableModel):
    '''
    With a custom "Tag" class, we can extend Tags to include other attributes, like a related department.

    "autocomplete_search_field" is required for AutocompletePanel on JanisBasePage; otherwise defaults to "title".
    '''
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    autocomplete_search_field = "name"
    def autocomplete_label(self):
        return self.name


# class TaggedPage(ItemBase):
#     '''
#     https://docs.wagtail.io/en/v2.10.1/reference/pages/model_recipes.html#custom-tag-models
#     '''
#     tag = models.ForeignKey(
#         PageTag, related_name="tagged_page", on_delete=models.CASCADE
#     )
#     content_object = ParentalKey(
#         to='base_page.JanisBasePage',
#         on_delete=models.CASCADE,
#         related_name='page_tags'
#     )
