import os
import graphene
import traceback

from django.db import models, ProgrammingError
from django.conf import settings
from wagtail.search import index
from wagtail.utils.decorators import cached_classmethod
from wagtail.admin.edit_handlers import FieldPanel, ObjectList, TabbedInterface
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from flags.state import flag_enabled

from base.models.site_settings import JanisBranchSettings

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

    notes_content_panel = [
        FieldPanel('author_notes')
    ]

    coa_global = models.BooleanField(default=False, verbose_name='Make this a top level page')

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
                'department page',
                'guide page',
                'official document page'
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
            # attributes for the url are needed by not discovered yet lets fetch them
            # looking for missing elements, deducing content type from what works and what dosen't
            # this is pretty ugly and ought to be cleaned up
            if theme_slug is None and self.content_type.name != 'department page':
                try:
                    theme_slug = self.topics.first().topic.topiccollections.first().topiccollection.theme.slug or None
                    topic_collection_slug = self.topics.first().topic.topiccollections.first().topiccollection.slug or None
                except AttributeError as e:
                    try:
                        theme_slug = self.topiccollections.first().topiccollection.theme.slug or None
                        topic_collection_slug = self.topiccollections.first().topiccollection.slug or None
                    except AttributeError as e:
                        # this is for pages just under departments
                        theme_slug = self.related_departments.all()[0].related_department.slug or None

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
            print(traceback.format_exc())
            return "#"
            pass

    # Optional "revision" parameter to get the janis_preview_url for a specific revision
    # Otherwise, it will return the janis_preview_url for the latest revision
    def janis_preview_url(self, revision=None):
        if revision:
            url_page_type = revision.page.janis_url_page_type
        else:
            revision = self.get_latest_revision()
            url_page_type = self.janis_url_page_type
        global_id = graphene.Node.to_global_id('PageRevisionNode', revision.id)
        base_url = self.janis_url_base()
        return base_url + "/en/preview/" + url_page_type + "/" + global_id

    # Default preview_url before janis_preview_url gets set
    def fallback_preview_url(self):
        return "https://alpha.austin.gov"

    # Use hardcoded JANIS_URL for staging and prod
    # Otherwise use configurable preview_janis_branch setting
    def janis_url_base(self):
        if settings.ISSTAGING or settings.ISPRODUCTION:
            return os.getenv("JANIS_URL")
        else:
            return JanisBranchSettings.objects.first().branch_preview_url_base()

    # data needed to construct preview URLs for any language
    # [janis_url_base]/[lang]/preview/[url_page_type]/[global_id]
    # ex: http://localhost:3000/es/preview/information/UGFnZVJldmlzaW9uTm9kZToyMjg=
    def preview_url_data(self):
        revision = self.get_latest_revision()
        global_id = graphene.Node.to_global_id('PageRevisionNode', revision.id)

        return {
            "janis_url_base": self.janis_url_base(),
            "url_page_type": self.janis_url_page_type,
            "global_id": global_id
        }

    @property
    def status_string(self):
        """
        override wagtail default
        see https://github.com/wagtail/wagtail/blob/f44d27642b4a6932de73273d8320bbcb76330c21/wagtail/core/models.py#L1010
        """
        if not self.live:
            if self.expired:
                return ("Expired")
            elif self.approved_schedule:
                return ("Scheduled")
            else:
                return ("Draft")
        else:
            if self.approved_schedule:
                return ("Live + Scheduled")
            elif self.has_unpublished_changes:
                return ("Live + Draft")
            else:
                return ("Live")

    @cached_classmethod
    def get_edit_handler(cls):
        if hasattr(cls, 'edit_handler'):
            return cls.edit_handler.bind_to_model(cls)

        editor_panels = [
            ObjectList(cls.content_panels + [AdminOnlyFieldPanel('coa_global', classname="admin-only-field")], heading='Content'),
            ObjectList(cls.notes_content_panel, heading='Notes')

        ]

        try:
            if flag_enabled('SHOW_EXTRA_PANELS'):
                editor_panels += (ObjectList(Page.promote_panels + cls.promote_panels,
                                             heading='SEO'),
                                  ObjectList(Page.settings_panels + cls.settings_panels,
                                             heading='Settings'))
        except ProgrammingError as e:
            print("some problem, maybe with flags")
            pass

        edit_handler = TabbedInterface(editor_panels)

        return edit_handler.bind_to_model(cls)

    class Meta:
        abstract = True


class AdminOnlyFieldPanel(FieldPanel):
    def render_as_object(self):
        if not self.request.user.is_superuser:
            return 'HIDE_ME'

        return super().render_as_object()
