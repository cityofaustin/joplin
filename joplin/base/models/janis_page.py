import os
import graphene


from django.db import models

from wagtail.search import index
from wagtail.utils.decorators import cached_classmethod

from wagtail.admin.edit_handlers import FieldPanel, ObjectList, TabbedInterface
from wagtail.admin.edit_handlers import FieldPanel, HelpPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField

"""
common fields shared by all pages
title

Homepage (index, list of themes & departments)
JanisBasePage:
    Theme (index, pages by theme) <--currently a snippet
        TopicCollection (index page, list of topics)
            TopicPage (list of pages by topic)
                related topic collections
                external services
                Shared between all ResidentPages:
                    Title
                    RelatedTopics
                    RelatedTopicsDepartment(s)
                    Top link
                    Author Notes
                    Contact(s) (except Docs page?)
                ServicePage
                InformationPage
                GuidePage
                DocumentPage
    Department (info about department, index of related services)
        ServicePage
        InformationPage
        GuidePage
        DocumentPage



"""


class JanisBasePage(Page):
    """
    This is base page class made for our pages to inherit from.
    It is abstract, which for Django means that it isn't stored as it's own table
    in the DB.
    We use it to add functionality that we know will be desired by all other pages,
    such as setting the preview fields and urls for janis stuff to make our headless
    setup work smoothly
    """

    subpage_types = []
    search_fields = Page.search_fields + [
        index.RelatedFields('owner', [
            index.SearchField('last_name', partial_match=True),
            index.FilterField('last_name'),
        ])
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)

    author_notes = RichTextField(
        # max_length=DEFAULT_MAX_LENGTH,
        features=['ul', 'ol', 'link'],
        blank=True,
        verbose_name='Notes for authors (Not visible on the resident facing site)'
    )

    def janis_url(self):
        """
        This function parses various attributes of related content types to construct the
        expected url structure for janis.

        For attributes with multiple relations, it ONLY takes the FIRST one.
        """

        try:
            """
             These use ternary operators with some appropriate conditionals
             the idea is: return this value in these cases or tell use you got
             nothing (see the privacy policy info page for example).

             'None' responses get filtered out and removed from the URL path.

             TODO:
             make this more abstract(potentially not by content type)
             further check if the order of conditionals affects performance
             Better utilization of querysets may be possible for better performance
            """
            page_slug = self.slug or None
            has_no_theme = [
                'service page',
                'topic page',
                'information page',
                'department page'
            ]
            has_no_topic_collection = has_no_theme

            has_no_topic = [
                'topic page',
                'topic collection page',
                'department page'
            ]

            theme_slug = (
                self.theme.slug
                if self.content_type.name not in has_no_theme
                else None
            )
            # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#first
            topic_collection_slug = (
                self.topiccollections.first().topiccollection.slug
                if
                (
                    self.content_type.name not in has_no_topic_collection and
                    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#exists
                    self.topiccollections.exists()
                )
                else None
            )
            topic_slug = (
                self.topics.first().topic.slug
                if
                (
                    self.content_type.name not in has_no_topic and
                    self.topics.exists()
                )
                else None
            )

            # add hardcoded language path to base url
            base_url = os.environ["JANIS_URL"] + '/en'
            # collect all our path elements
            paths_list = [
                base_url,
                theme_slug,
                topic_collection_slug,
                topic_slug,
                page_slug]
            # join them together, filtering out empty ones
            janis_url = '/'.join(filter(None, (paths_list)))
            return janis_url
        except Exception as e:
            # right now this is a catch-all,
            print("!janis url error!:", self.title, e)
            return "#"
            pass

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

    content_panels = [
        FieldPanel('title_en'),
        FieldPanel('title_es'),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description')
    ]

    @cached_classmethod
    def get_edit_handler(cls):
        """
        this appears to be for setting up previews via the api,
        but could/should probably be revisited
        """
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
