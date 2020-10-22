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


class JanisBasePage(Page):
    """
    This is base page class made for our pages to inherit from.
    It is abstract, which for Django means that it isn't stored as it's own table
    in the DB.
    We use it to add functionality that we know will be desired by all other pages,
    such as setting the preview fields and urls for janis stuff to make our headless
    setup work smoothly
    """

    parent_page_types = ['home_page.HomePage']
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
    imported_revision_id = models.TextField(blank=True, null=True)

    # Fields used for handling Publishing status
    # pk for our publish request in Publisher dynamodb
    publish_request_pk = models.TextField(blank=True, null=True)
    # sk for our publish request in Publisher dynamodb
    publish_request_sk = models.TextField(blank=True, null=True)
    # Indicates whether a publish_request for this page been submitted to the Publisher, and we are
    # waiting for it to finish being processed.
    publish_request_enqueued = models.BooleanField(default=False)
    # Has this page been published by Publisher? A "live" page may not necessarily be published to our frontend yet.
    published = models.BooleanField(default=False, blank=True, null=True)

    # Used to display search_summary field in search results. Defaults to empty string
    @property
    def search_summary(self):
        return ""

    def janis_urls(self):
        """
        Returns list of page urls (strings)
        If page is global, returns slug
        Otherwise returns a list of department/slug for each department
        """
        # If we're global, even if we have a department, we should only exist at
        # /page_slug
        # and not at
        # /department_slug/page_slug
        if self.coa_global:
            return [f'/{self.slug}/']

        # If we're under departments
        departments = self.departments()
        if len(departments) > 0:
            return [f'/{department.slug_en}/{self.slug_en}/'
                    for department in departments
                    ]

        # make sure we return an empty array if we don't have any urls
        return []

    def janis_instances(self):
        """
        Returns list of page urls
        If page is global, returns slug
        Otherwise returns department/slug for each department
        """
        # If we're global, even if we have a department, we should only exist at
        # /page_slug
        # and not at
        # /department_slug/page_slug
        if self.coa_global:
            return [{'url': f'{self.slug}/', 'parent': None, 'grandparent': None}]

        # If we're under departments
        departments = self.departments()
        if len(departments) > 0:
            return [
                {'url': f'/{department.slug_en}/{self.slug_en}/',
                 'parent': department,
                 'grandparent': None}
                for department in departments
            ]

        # make sure we return an empty array if we don't have any urls
        return []

    def janis_preview_url_end(self, revision=None):
        """
            Optional "revision" parameter to get the janis_preview_url for a specific revision
            Otherwise, it will return the janis_preview_url for the latest revision
        """
        if revision:
            url_page_type = revision.page.janis_url_page_type
        else:
            revision = self.get_latest_revision()
            url_page_type = self.janis_url_page_type
        try:
            global_id = graphene.Node.to_global_id('PageRevisionNode', revision.id)
            url_end = f"preview/{url_page_type}/{global_id}"
        except AttributeError:
            # TODO: make previews work for test fixture pages that may not have revisions/global_ids
            url_end = f"preview/{url_page_type}/"

        if settings.IS_STAGING or settings.IS_PRODUCTION:
            return url_end
        else:
            # Pass address of CMS_API if we are not running on Staging or Production
            # Janis will query from its default CMS_API if a param is not provided
            return url_end + f"?PREVIEW_CMS_API={settings.PREVIEW_CMS_API}"

    def preview_url_data(self, revision=None):
        """
        :param revision: optional
        :return: Returns data needed to construct preview URLs for any language.
        This is used both in base_page/models.py and on the frontend edit page django template.
        [janis_preview_url_start]/[lang]/[janis_preview_url_end]
        ex: http://localhost:3000/es/preview/information/UGFnZVJldmlzaW9uTm9kZToyMjg=
        """
        return {
            "janis_preview_url_start": self.get_parent().specific.preview_url_base(),
            "janis_preview_url_end": self.janis_preview_url_end(revision=revision),
        }

    def janis_preview_url(self, revision=None, lang="en"):
        data = self.preview_url_data(revision)
        return f'{data["janis_preview_url_start"]}/{lang}/{data["janis_preview_url_end"]}'

    def janis_publish_url(self):
        """
        Used by page_status_tag.html
        :return: the first janis_url path for now
        """
        paths = self.janis_urls()
        if len(paths) > 0:
            first_path = paths[0]
            parent_home_page = self.get_parent()
            if parent_home_page:
                return f'{parent_home_page.specific.publish_url_base()}{first_path}'
        # Default to returning same page as url
        return "#"

    @property
    def status_string(self):
        """
        override wagtail default
        see https://github.com/wagtail/wagtail/blob/f44d27642b4a6932de73273d8320bbcb76330c21/wagtail/core/models.py#L1010
        """
        if self.live:
            if self.published:
                if self.publish_request_enqueued:
                    # A page is live, already published, and now publishing an update
                    return "Live + Publishing"
                else:
                    if self.has_unpublished_changes:
                        # A page is live and published, with a new draft revision in progress
                        return "Live + Draft"
                    else:
                        # A page is live and published
                        return "Live"
            else:
                # A page is live and about to be published for the first time
                return "Publishing"
        else:
            if self.published:
                # A page is still up, but is now unpublishing
                return "Live + Unpublishing"
            else:
                # A page is not live and not published
                return "Draft"

    def departments(self):
        """
         This goes through our group page permissions and looks for any related departments
         If the department does not have a department page associated with it, it will not return
        :return: list of DepartmentPages
        """
        department_pages = []
        for group_permission in self.group_permissions.all():
            if (group_permission and
                group_permission.group and
                group_permission.group.department and
                    group_permission.group.department.department_page):
                department_pages.append(group_permission.group.department.department_page)
        return department_pages

    @cached_classmethod
    def get_edit_handler(cls):
        if hasattr(cls, 'edit_handler'):
            return cls.edit_handler.bind_to(model=cls)

        editor_panels = [
            ObjectList(cls.content_panels + [AdminOnlyFieldPanel('coa_global', classname="admin-only-field")],
                       heading='Content'),
            ObjectList(cls.notes_content_panel, heading='Notes')

        ]

        try:
            if flag_enabled('SHOW_EXTRA_PANELS'):
                editor_panels += [PermissionObjectList(cls.settings_panels,
                                                       heading='Settings')]
                # editor_panels += (PermissionObjectList(cls.promote_panels,
                #                                        heading='SEO'),
                #                   PermissionObjectList(cls.settings_panels,
                #                                        heading='Settings'))
        except ProgrammingError as e:
            print("some problem, maybe with flags")
            print(traceback.format_exc())
            pass

        edit_handler = TabbedInterface(editor_panels)

        return edit_handler.bind_to(model=cls)

    def with_content_json(self, content_json):
        obj = super().with_content_json(content_json)
        # Ensure other values that are meaningful for the page as a whole (rather than
        # to a specific revision) are preserved
        obj.publish_request_pk = self.publish_request_pk
        obj.publish_request_sk = self.publish_request_sk
        obj.publish_request_enqueued = self.publish_request_enqueued
        obj.published = self.published

        return obj

    class Meta:
        # https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#custom-permissions
        permissions = [
            ("view_extra_panels", "Can view extra panels"),
            ("view_snippets", "Can view snippets"),
            ("add_snippets", "Can add snippet"),
            ("delete_snippets", "Can delete snippet"),
        ]


class AdminOnlyFieldPanel(FieldPanel):
    def on_form_bound(self):
        model_name = self.model.__name__
        self.bound_field = self.form[self.field_name]
        self.help_text = self.bound_field.help_text
        # If user is superuser and page is Service Page or Information Page
        # show the field panel text "Make This a Top Level Page"
        if self.request.user.is_superuser:
            if model_name is 'ServicePage' or model_name is 'InformationPage':
                self.heading = self.bound_field.label
            else:
                self.heading = ""
        else:
            self.heading = ""

    def render_as_object(self):
        model_name = self.model.__name__
        # Checks to see if user is super user, if so render object
        # if not, return empty string which overrides the object/checkbox
        if not self.request.user.is_superuser:
            return ''
        if model_name is not 'ServicePage' and model_name is not 'InformationPage':
            return ''

        return super().render_as_object()


class PermissionObjectList(ObjectList):
    def __init__(self, children=(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hide_panel = True
        self.children = children

    def on_form_bound(self):
        if self.request.user.has_perm('base_page.view_extra_panels'):
            # tabbed_interface.html checks to see if the panel should be hid
            # and if so prevents the tab from being added
            self.hide_panel = False
        return super().on_form_bound()

    # def render(self):
    #     # this only hides the content of the tab, not the tab/heading itself
    #     if not self.request.user.has_perm('base_page.view_extra_panels'):
    #         return ""
    #
    #     return super().render()
