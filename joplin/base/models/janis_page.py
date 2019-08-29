import os
import graphene


from django.db import models

from wagtail.search import index
from wagtail.utils.decorators import cached_classmethod

from wagtail.admin.edit_handlers import FieldPanel, ObjectList, TabbedInterface

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField


class JanisBasePage(Page):
    """
    This is base page class made for our pages to inherit from.
    It is abstract, which for Django means that it isn't stored as it's own table
    in the DB.
    We use it to add functionality that we know will be desired by all other pages,
    such as setting the preview fields and urls for janis stuff to make our headless
    setup work smoothly
    """

    parent_page_types = ['base.HomePage']
    subpage_types = []
    search_fields = Page.search_fields + [
        index.RelatedFields('owner', [
            index.SearchField('last_name', partial_match=True),
            index.FilterField('last_name'),
        ])
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author_notes = RichTextField(
        # max_length=DEFAULT_MAX_LENGTH,
        features=['ul', 'ol', 'link'],
        blank=True,
        verbose_name='Notes for authors (Not visible on the resident facing site)'
    )

    def janis_url(self):
        page_slug = self.slug

        if self.janis_url_page_type == "department":

            return os.environ["JANIS_URL"] + "/en/" + page_slug

        if self.janis_url_page_type == "topiccollection":
            try:
                theme_slug = self.theme.slug
                return os.environ["JANIS_URL"] + "/en/" + theme_slug + "/" + page_slug
            except Exception as e:
                pdb.set_trace()
                print("!janis url error!:", self.title, e)

        if self.janis_url_page_type == "topic":
            # If we have a topic collection
            try:
                if self.topiccollections:
                    primary_topic_collection = self.topiccollections.first().topiccollection
                    theme_slug = primary_topic_collection.theme.slug
                    topic_collection_slug = primary_topic_collection.slug
                    return os.environ["JANIS_URL"] + "/en/" + theme_slug + "/" + topic_collection_slug + "/" + page_slug
            except Exception as e:
                pdb.set_trace()
                print("!janis url error!:", self.title, e)

        if self.janis_url_page_type == "services" or self.janis_url_page_type == "information" or janis_url_page_type == "guide":
            # If we have topics, use the first one
            try:
                # this is wasteful but needed for info page edge case
                if self.topics.first():
                    primary_topic = self.topics.first().topic
                    topic_slug = primary_topic.slug
                    # Make sure we have a topic collection too
                    if primary_topic.topiccollections:
                        primary_topic_collection = primary_topic.topiccollections.first().topiccollection
                        theme_slug = primary_topic_collection.theme.slug
                        topic_collection_slug = primary_topic_collection.slug
                        return os.environ["JANIS_URL"] + "/en/" + theme_slug + "/" + topic_collection_slug + "/" + topic_slug + "/" + page_slug
            except Exception as e:
                import pdb
                pdb.set_trace()
                print("!janis url error!:", self.title, e)

            # TODO: bring back departments now that we can have multiple

        # We don't have a valid live url
        # TODO: add something to make this clear to users
        return "#"

    def janis_preview_url(self):
        revision = self.get_latest_revision()
        url_page_type = self.janis_url_page_type
        global_id = graphene.Node.to_global_id('PageRevisionNode', revision.id)

        return os.environ["JANIS_URL"] + "/en/preview/" + url_page_type + "/" + global_id

    # Default preview_url before janis_preview_url gets set
    def fallback_preview_url(self):
        return "https://alpha.austin.gov"

    # data needed to construct preview URLs for any language
    # [janis_url_base]/[lang]/preview/[url_page_type]/[global_id]
    # ex: http://localhost:3000/es/preview/information/UGFnZVJldmlzaW9uTm9kZToyMjg=
    def preview_url_data(self):
        revision = self.get_latest_revision()
        global_id = graphene.Node.to_global_id('PageRevisionNode', revision.id)

        return {
            "janis_url_base": os.environ["JANIS_URL"],
            "url_page_type": self.janis_url_page_type,
            "global_id": global_id
        }

    @cached_classmethod
    def get_edit_handler(cls):
        if hasattr(cls, 'edit_handler'):
            return cls.edit_handler.bind_to_model(cls)

        edit_handler = TabbedInterface([
            ObjectList(cls.content_panels + [
                FieldPanel('author_notes')
            ], heading='Content'),
            ObjectList(Page.promote_panels + cls.promote_panels, heading='Search Info')
        ])

        return edit_handler.bind_to_model(cls)

    class Meta:
        abstract = True
