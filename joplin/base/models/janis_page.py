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
        """
        This function parses various attributes of content types to construct the
        expected url structure for janis
         It probably could use some refactoring.
        """
        page_slug = self.slug
        content_type = self.content_type.name

        try:
            if content_type == "department page":

                return os.environ["JANIS_URL"] + "/en/" + page_slug

            elif content_type== "topic collection page":
                theme_slug = self.theme.slug
                return os.environ["JANIS_URL"] + "/en/" + theme_slug + "/" + page_slug
            elif content_type== "topic page":
                # If we have a topic collection
                if self.topiccollections:
                    primary_topic_collection = self.topiccollections.first().topiccollection
                    theme_slug = primary_topic_collection.theme.slug
                    topic_collection_slug = primary_topic_collection.slug
                    return os.environ["JANIS_URL"] + "/en/" + theme_slug + "/" + topic_collection_slug + "/" + page_slug
            elif content_type in ["service page", "information page", "guide page"]:
                if self.topics.first():
                    primary_topic = self.topics.first().topic
                    topic_slug = primary_topic.slug
                    # Make sure we have a topic collection too
                    if primary_topic.topiccollections:
                        primary_topic_collection = primary_topic.topiccollections.first().topiccollection
                        theme_slug = primary_topic_collection.theme.slug
                        topic_collection_slug = primary_topic_collection.slug
                        return os.environ["JANIS_URL"] + "/en/" + theme_slug + "/" + topic_collection_slug + "/" + topic_slug + "/" + page_slug
            else:
                return "#"
        except Exception as e:
            print("!janis url error!:", self.title, e)
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
            ObjectList(Page.promote_panels + cls.promote_panels,
                       heading='Search Info')
        ])

        return edit_handler.bind_to_model(cls)

    class Meta:
        abstract = True
