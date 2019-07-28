from django.db import models
import os
import graphene

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.utils.decorators import cached_classmethod
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface, HelpPanel
from wagtail.core.blocks import TextBlock, RichTextBlock, ListBlock, StreamBlock, StructBlock, URLBlock, PageChooserBlock, CharBlock, DateBlock
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.admin.edit_handlers import PageChooserPanel

from . import blocks as custom_blocks
from . import forms as custom_forms

WYSIWYG_GENERAL = ['h1', 'h2', 'h3', 'h4', 'bold', 'link', 'ul', 'ol', 'code']
WYSIWYG_SERVICE_STEP = ['ul', 'ol', 'link', 'code']
DEFAULT_MAX_LENGTH = 255
SHORT_DESCRIPTION_LENGTH = 300

class TranslatedImage(AbstractImage):
    admin_form_fields = Image.admin_form_fields

    def __str__(self):
        return self.title or self.title_en


class TranslatedImageRendition(AbstractRendition):
    image = models.ForeignKey(TranslatedImage, related_name='renditions', on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )

@register_snippet
class ThreeOneOne(ClusterableModel):
    title = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    url = models.URLField()

    def __str__(self):
        return self.title


class HomePage(Page):
    parent_page_types = []
    # subpage_types = ['base.ServicePage', 'base.ProcessPage', 'base.InformationPage', 'base.DepartmentPage']
    subpage_types = ['base.ServicePage', 'base.ProcessPage', 'base.InformationPage', 'base.DepartmentPage', 'base.TopicPage']

    image = models.ForeignKey(TranslatedImage, null=True, on_delete=models.SET_NULL, related_name='+')


class JanisBasePage(Page):
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
            theme_slug = self.theme.slug;
            return os.environ["JANIS_URL"] + "/en/" + theme_slug + "/" + page_slug

        if self.janis_url_page_type == "topic":
            # If we have a topic collection
            if self.topiccollections and self.topiccollections.all():
                theme_slug = self.topiccollections.all()[0].topiccollection.theme.slug;
                tc_slug = self.topiccollections.all()[0].topiccollection.slug;
                return os.environ["JANIS_URL"] + "/en/" + theme_slug + "/" + tc_slug + "/" + page_slug


        if self.janis_url_page_type == "services" or self.janis_url_page_type == "information":
            # If we have topics, use the first one
            if self.topics and self.topics.all():
                topic_slug = self.topics.all()[0].topic.slug
                # Make sure we have a topic collection too
                if self.topics.all()[0].topic.topiccollections.all():
                    theme_slug = self.topics.all()[0].topic.topiccollections.all()[0].topiccollection.theme.slug;
                    tc_slug = self.topics.all()[0].topic.topiccollections.all()[0].topiccollection.slug;
                    return os.environ["JANIS_URL"] + "/en/" + theme_slug + "/" + tc_slug + "/" + topic_slug + "/" + page_slug

            # If we have a department, use that
            if self.department:
                return os.environ["JANIS_URL"] + "/en/" + self.department.slug + "/" + page_slug

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

    class Meta:
        abstract = True

class JanisPage(JanisBasePage):
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

class ServicePage(JanisPage):
    janis_url_page_type = "services"

    department = models.ForeignKey(
        'base.DepartmentPage',
        on_delete=models.PROTECT,
        verbose_name='Select a Department',
        blank=True,
        null=True,
    )

    steps = StreamField(
        [
            ('basic_step', RichTextBlock(
                features=WYSIWYG_SERVICE_STEP,
                label='Basic Step'
            )),
            ('step_with_options_accordian', StructBlock(
                [
                    ('options_description', TextBlock('Describe the set of options')),
                    ('options', ListBlock(
                        StructBlock([
                            ('option_name', TextBlock(
                                label='Option name. (When clicked, this name will expand the content for this option'
                            )),
                            ('option_description', RichTextBlock(
                                features=WYSIWYG_SERVICE_STEP,
                                label='Option Content',
                            )),
                        ]),
                    )),
                ],
                label="Step With Options"
            )),
        ],
        verbose_name='Write out the steps a resident needs to take to use the service',
        # this gets called in the help panel
        help_text='A step may have a basic text step or an options accordion which reveals two or more options',
        blank=True
    )

    dynamic_content = StreamField(
        [
            ('map_block', custom_blocks.SnippetChooserBlockWithAPIGoodness('base.Map', icon='site')),
            ('what_do_i_do_with_block', custom_blocks.WhatDoIDoWithBlock()),
            ('collection_schedule_block', custom_blocks.CollectionScheduleBlock()),
            ('recollect_block', custom_blocks.RecollectBlock()),
        ],
        verbose_name='Add any maps or apps that will help the resident use the service',
        blank=True
    )
    additional_content = RichTextField(
        features=WYSIWYG_GENERAL,
        verbose_name='Write any additional content describing the service',
        help_text='Section header: What else do I need to know?',
        blank=True
    )

    base_form_class = custom_forms.ServicePageForm

    short_description = models.TextField(
        max_length=SHORT_DESCRIPTION_LENGTH,
        blank=True,
        verbose_name='Write a description of this service'
    )

    content_panels = [
        FieldPanel('title_en'),
        FieldPanel('title_es'),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('short_description'),
        InlinePanel('topics', label='Topics'),
        FieldPanel('department'),
        InlinePanel('related_departments', label='Related Departments'),
        MultiFieldPanel(
        [
            HelpPanel(steps.help_text, classname="coa-helpPanel"),
            StreamFieldPanel('steps')
        ],
        heading=steps.verbose_name,
        classname='coa-multiField-nopadding'
        ),
        StreamFieldPanel('dynamic_content'),
        MultiFieldPanel(
        [
            HelpPanel(additional_content.help_text, classname="coa-helpPanel"),
            FieldPanel('additional_content')
        ],
        heading=additional_content.verbose_name,
        classname='coa-multiField-nopadding'
        )
        ,
        InlinePanel('contacts', label='Contacts'),
    ]


class ProcessPage(JanisPage):
    janis_url_page_type = "processes"

    department = models.ForeignKey(
        'base.DepartmentPage',
        on_delete=models.PROTECT,
        verbose_name='Select a Department',
        blank=True,
        null=True,
    )

    description = models.TextField(blank=True)
    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    # TODO: Add images array field

    base_form_class = custom_forms.ProcessPageForm

    content_panels = [
        InlinePanel('topics', label='Topics'),
        FieldPanel('department'),
        FieldPanel('description'),
        ImageChooserPanel('image'),
        InlinePanel('contacts', label='Contacts'),
        InlinePanel('process_steps', label="Process steps"),
    ]

class InformationPage(JanisPage):
    janis_url_page_type = "information"

    department = models.ForeignKey(
        'base.DepartmentPage',
        on_delete=models.PROTECT,
        verbose_name='Select a Department',
        blank=True,
        null=True,
    )

    description = models.TextField(blank=True, verbose_name='Write a description of this page')
    options = StreamField(
        [
            ('option', RichTextBlock(
                features=WYSIWYG_GENERAL,
                label='Option'
            ))
        ],
        verbose_name='Add option sections as needed.',
        help_text='Options are needed when the reader needs to make a choice between a few options, such as ways to fill out a form (online, by phone, in person, etc.).',
        blank=True
    )

    additional_content = RichTextField(
        features=WYSIWYG_GENERAL,
        verbose_name='Write any additional content describing the service',
        blank=True
    )

    # TODO: Add images array field

    base_form_class = custom_forms.InformationPageForm

    content_panels = [
        FieldPanel('title_en'),
        FieldPanel('title_es'),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        InlinePanel('topics', label='Topics'),
        FieldPanel('department'),
        InlinePanel('related_departments', label='Related Departments'),
        FieldPanel('description'),
        StreamFieldPanel('options'),
        FieldPanel('additional_content'),
        InlinePanel('contacts', label='Contacts'),
    ]

class TopicCollectionPage(JanisPage):
    janis_url_page_type = "topiccollection"

    description = models.TextField(blank=True)


    theme = models.ForeignKey(
        'base.Theme',
        on_delete=models.PROTECT,
        related_name='topicCollectionPages',
        null=True, blank=True,
    )

    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    base_form_class = custom_forms.TopicCollectionPageForm

    content_panels = [
        FieldPanel('title_en'),
        FieldPanel('title_es'),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description'),
        FieldPanel('theme'),
        ImageChooserPanel('image'),
        InlinePanel('topiccollections', label='Topic Collections this page belongs to'),
    ]

class TopicPage(JanisPage):
    janis_url_page_type = "topic"

    description = models.TextField(blank=True)

    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    external_services = StreamField(
        [
            ('link_en', StructBlock([
                ('url', URLBlock()),
                ('title', CharBlock()),
            ], icon='link', label='Link [EN]')),
            ('link_es', StructBlock([
                ('url', URLBlock()),
                ('title', CharBlock()),
            ], icon='link', label='Link [ES]')),
            ('link_ar', StructBlock([
                ('url', URLBlock()),
                ('title', CharBlock()),
            ], icon='link', label='Link [AR]')),
            ('link_vi', StructBlock([
                ('url', URLBlock()),
                ('title', CharBlock()),
            ], icon='link', label='Link [VI]')),
        ],
        verbose_name='External links to services',
        blank=True
    )

    base_form_class = custom_forms.TopicPageForm

    content_panels = [
        FieldPanel('title_en'),
        FieldPanel('title_es'),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description'),
        ImageChooserPanel('image'),
        StreamFieldPanel('external_services'),
        InlinePanel('topiccollections', label='Topic Collections this page belongs to'),
    ]

class DepartmentPage(JanisPage):
    janis_url_page_type = "department"

    def __str__(self):
        return self.title_en

    what_we_do = RichTextField(
        features=WYSIWYG_GENERAL,
        verbose_name='What we do',
        blank=True
    )

    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    mission = models.TextField(
        verbose_name='Mission',
    )

    job_listings = models.URLField(
        verbose_name='Job listings url',
        help_text='Link to a page with job listings.',
        blank=True
    )

    top_services = StreamField(
        [
            ('link_en', StructBlock([
                ('url', URLBlock()),
                ('title', CharBlock()),
            ], icon='link', label='Link [EN]')),
            ('link_es', StructBlock([
                ('url', URLBlock()),
                ('title', CharBlock()),
            ], icon='link', label='Link [ES]')),
            ('link_ar', StructBlock([
                ('url', URLBlock()),
                ('title', CharBlock()),
            ], icon='link', label='Link [AR]')),
            ('link_vi', StructBlock([
                ('url', URLBlock()),
                ('title', CharBlock()),
            ], icon='link', label='Link [VI]')),
            # ('page', PageChooserBlock(
            #     label='Choose a page',
            #     icon='doc-full'
            # ))
        ],
        verbose_name='Links to top services',
        blank=True
    )

    base_form_class = custom_forms.DepartmentPageForm

    content_panels = [
        FieldPanel('title_en'),
        FieldPanel('title_es'),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('what_we_do'),
        ImageChooserPanel('image'),
        FieldPanel('mission'),
        InlinePanel('contacts', label='Contacts'),
        InlinePanel('department_directors', label="Department Directors"),
        FieldPanel('job_listings'),
        StreamFieldPanel('top_services'),
    ]

class DepartmentPageDirector(Orderable):
    page = ParentalKey(DepartmentPage, related_name='department_directors')
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    title = models.CharField(max_length=DEFAULT_MAX_LENGTH, default='Director')
    photo = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    about = models.TextField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('title'),
        ImageChooserPanel('photo'),
        FieldPanel('about'),
    ]

class OfficialDocumentPage(JanisPage):
    janis_url_page_type = "official_document"
    base_form_class = custom_forms.OfficialDocumentPageForm

    description = models.TextField(blank=True)

    department = models.ForeignKey(
        'base.DepartmentPage',
        on_delete=models.PROTECT,
        verbose_name='Select a Department',
        blank=True,
        null=True,
    )

    documents = StreamField(
        [
            ('document', StructBlock(
                [
                    ('date', DateBlock(label="Document date")),
                    ('title', CharBlock(label="Document title")),
                    ('authoring_office', CharBlock(label="Authoring office of document")),
                    ('summary', TextBlock(label="Document summary", max_length=600, classname="streamfield-textblock", help_text="600 char limit")),
                    ('name', CharBlock(label="Name of Document")),
                    ('link', URLBlock(label="Link to Document (URL)"))
                ]
            )),
        ],
        verbose_name="Entries will be listed by document date (newest first).",
        blank=True,
    )

    content_panels = [
        FieldPanel('title_en'),
        FieldPanel('title_es'),
        FieldPanel('title_ar'),
        FieldPanel('title_vi'),
        FieldPanel('description'),
        InlinePanel('topics', label='Topics'),
        FieldPanel('department'),
        InlinePanel('related_departments', label='Related Departments'),
        # MultiFieldPanel(
        #     [
        #         StreamFieldPanel('documents')
        #     ],
        #     heading=documents.verbose_name,
        #     classname='coa-multiField-nopadding'
        # ),
        StreamFieldPanel('documents'),
    ]

class ProcessPageStep(Orderable):
    page = ParentalKey(ProcessPage, related_name='process_steps')
    title = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    short_title = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    link_title = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    description = models.TextField(blank=True)
    image = models.ForeignKey(TranslatedImage, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    overview_steps = RichTextField(features=WYSIWYG_GENERAL, verbose_name='Write out the steps a resident needs to take to use the service', blank=True)
    detailed_content = RichTextField(features=WYSIWYG_GENERAL, verbose_name='Write any detailed content describing the process', blank=True)
    quote = models.TextField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('short_title'),
        FieldPanel('link_title'),
        FieldPanel('description'),
        ImageChooserPanel('image'),
        FieldPanel('overview_steps'),
        FieldPanel('detailed_content'),
        FieldPanel('quote'),
    ]


@register_snippet
class Theme(ClusterableModel):
    slug = models.SlugField()
    text = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    description = models.TextField()

    def __str__(self):
        return self.text


@register_snippet
class Map(ClusterableModel):
    description = models.TextField()
    location = models.ForeignKey('base.Location', on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.description

    def serializable_data(self):
        data = {
            'location': self.location.serializable_data(),
            'description': self.description,
        }

        data['location'].pop('pk')

        return data


@register_snippet
class Location(ClusterableModel):
    TX = 'TX'
    STATE_CHOICES = (
        (TX, 'Texas'),
    )

    USA = 'United States'
    COUNTRY_CHOICES = (
        (USA, 'United States'),
    )

    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    street = models.TextField()
    city = models.CharField(max_length=DEFAULT_MAX_LENGTH, default='Austin')
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default=TX)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, default=USA)
    zip = models.CharField(max_length=50)

    panels = [
        FieldPanel('name'),
        MultiFieldPanel(children=[
            FieldPanel('street'),
            FieldPanel('city', classname='col5'),
            FieldPanel('state', classname='col4'),
            FieldPanel('zip', classname='col2'),
            FieldPanel('country', classname='col5'),
        ], heading='Location'),
    ]

    def __str__(self):
        return self.name


class DayAndDuration(ClusterableModel):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'
    DAY_OF_WEEK_CHOICES = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )

    day_of_week = models.CharField(max_length=20, choices=DAY_OF_WEEK_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    content_panels = [
        FieldPanel('day_of_week'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
    ]

    def __str__(self):
        return f'{self.day_of_week} {self.start_time} - {self.end_time}'


@register_snippet
class Contact(ClusterableModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    email = models.EmailField()
    phone = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    location = models.ForeignKey(Location, null=True, blank=True, related_name='+', on_delete=models.SET_NULL)

    social_media = StreamField(
        [
            ('url', URLBlock(
                label='Social media url'
            ))
        ],
        verbose_name='Links to any social media pages',
        help_text='For example: https://www.facebook.com/atxpoliceoversight/',
        blank=True
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('email'),
        FieldPanel('phone'),
        SnippetChooserPanel('location'),
        InlinePanel('hours', label='Hours'),
        StreamFieldPanel('social_media'),
    ]

    def __str__(self):
        return self.name


class ContactDayAndDuration(Orderable, DayAndDuration):
    contact = ParentalKey(Contact, related_name='hours')

    content_panels = [
        SnippetChooserPanel('day_and_duration'),
    ]


class ProcessPageContact(ClusterableModel):
    process = ParentalKey(ProcessPage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name

class ProcessPageTopic(ClusterableModel):
    page = ParentalKey(ProcessPage, related_name='topics')
    topic = models.ForeignKey('base.TopicPage',  verbose_name='Select a Topic', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topic'),
    ]

    def __str__(self):
        return self.topic.text

class ServicePageContact(ClusterableModel):
    page = ParentalKey(ServicePage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name

class ServicePageRelatedDepartments(ClusterableModel):
    page = ParentalKey(ServicePage, related_name='related_departments', default=None)
    related_department = models.ForeignKey(
        "base.departmentPage",
        on_delete=models.PROTECT,
    )

    panels = [
        # Use a SnippetChooserPanel because blog.BlogAuthor is registered as a snippet
        PageChooserPanel("related_department"),
    ]

class InformationPageRelatedDepartments(ClusterableModel):
    page = ParentalKey(InformationPage, related_name='related_departments', default=None)
    related_department = models.ForeignKey(
        "base.departmentPage",
        on_delete=models.PROTECT,
    )

    panels = [
        # Use a SnippetChooserPanel because blog.BlogAuthor is registered as a snippet
        PageChooserPanel("related_department"),
    ]

class OfficialDocumentPageRelatedDepartments(ClusterableModel):
    page = ParentalKey(OfficialDocumentPage, related_name='related_departments', default=None)
    related_department = models.ForeignKey(
        "base.departmentPage",
        on_delete=models.PROTECT,
    )

    panels = [
        # Use a SnippetChooserPanel because blog.BlogAuthor is registered as a snippet
        PageChooserPanel("related_department"),
    ]

class TopicCollectionPageTopicCollection(ClusterableModel):
    page = ParentalKey(TopicCollectionPage, related_name='topiccollections')
    topiccollection = models.ForeignKey('base.TopicCollectionPage',  verbose_name='Select a Topic Collection', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topiccollection'),
    ]

    def __str__(self):
        return self.topiccollection.text

class TopicPageTopicCollection(ClusterableModel):
    page = ParentalKey(TopicPage, related_name='topiccollections')
    topiccollection = models.ForeignKey('base.TopicCollectionPage',  verbose_name='Select a Topic Collection', related_name='+', on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('topiccollection'),
    ]

    def __str__(self):
        return self.topiccollection.text

class ServicePageTopic(ClusterableModel):
    page = ParentalKey(ServicePage, related_name='topics')
    topic = models.ForeignKey('base.TopicPage',  verbose_name='Select a Topic', related_name='+', on_delete=models.CASCADE)
    toplink = models.BooleanField(default=False, verbose_name='Make this service a top link for this topic')

    panels = [
        MultiFieldPanel(
            [
                PageChooserPanel('topic'),
                FieldPanel('toplink'),
            ]
        ),
    ]

    def __str__(self):
        return self.topic.title

class InformationPageContact(ClusterableModel):
    page = ParentalKey(InformationPage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name

class InformationPageTopic(ClusterableModel):
    page = ParentalKey(InformationPage, related_name='topics')
    topic = models.ForeignKey('base.TopicPage',  verbose_name='Select a Topic', related_name='+', on_delete=models.CASCADE)
    toplink = models.BooleanField(default=False, verbose_name='Make this page a top link for this topic')

    panels = [
        MultiFieldPanel(
            [
                PageChooserPanel('topic'),
                FieldPanel('toplink'),
            ]
        ),
    ]

    def __str__(self):
        return self.topic.text

class OfficialDocumentPageTopic(ClusterableModel):
    page = ParentalKey(OfficialDocumentPage, related_name='topics')
    topic = models.ForeignKey('base.TopicPage',  verbose_name='Select a Topic', related_name='+', on_delete=models.CASCADE)
    toplink = models.BooleanField(default=False, verbose_name='Make this list a top link for this topic')

    panels = [
        MultiFieldPanel(
            [
                PageChooserPanel('topic'),
                FieldPanel('toplink'),
            ]
        ),
    ]

    def __str__(self):
        return self.topic.text

class DepartmentPageContact(ClusterableModel):
    page = ParentalKey(DepartmentPage, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.contact.name

@register_snippet
class Department(ClusterableModel):
    slug = models.SlugField()
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    mission = models.TextField()
    image = models.ForeignKey(TranslatedImage, null=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        FieldPanel('name'),
        FieldPanel('mission'),
        InlinePanel('contacts', label='Contacts'),
        ImageChooserPanel('image'),
    ]

    def __str__(self):
        return self.name


class DepartmentContact(ClusterableModel):
    department = ParentalKey(Department, related_name='contacts')
    contact = models.ForeignKey(Contact, related_name='+', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('contact'),
    ]

    def __str__(self):
        return self.department.name
