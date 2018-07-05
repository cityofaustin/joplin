from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html_join

from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.core import hooks

from base.models import Topic, Location, Contact
from wagtail.admin.site_summary import SummaryItem, PagesSummaryItem
from wagtail.images.wagtail_hooks import ImagesMenuItem

from django.utils.safestring import mark_safe

# adjust homepage panel content
class WelcomePanel:
    order = 500

    def render(self):
        return mark_safe("""
            <section class="panel summary nice-padding">
              <h3>No, but seriously -- Butts.</h3>
            </section>
            <h1>%s</h1>
            <div>%s</div>
            """ % ('hooks', list(hooks._hooks))
        )

@hooks.register('construct_homepage_panels')
def add_another_welcome_panel(request, panels):
    return panels.append( WelcomePanel() )


# adjust homepage summary content
class MyFunkyItem(PagesSummaryItem):
    def render(self):
        return 'Butts'


@hooks.register('construct_homepage_summary_items', order=500)
def add_summary_item(request, summary_items):
    summary_items.append(MyFunkyItem(request));

# adjust left nav content
@hooks.register('construct_main_menu', order=6000)
def remove_menu_item(request, menu_items):
    for item in list(menu_items):
        if not isinstance(item, ImagesMenuItem):
            menu_items.remove(item)

@hooks.register('insert_editor_css')
def editor_css():
    urls = [
        static('css/admin.css'),
        static('css/toggle.css'),
        static('css/preview.css'),
    ]
    return format_html_join('\n', '<link rel="stylesheet" href="{}">', ((url,) for url in urls))


@hooks.register('insert_global_admin_js')
def global_admin_js():
    urls = []

    if settings.USE_ANALYTICS:
        urls.append(static('js/analytics.js'))

    return format_html_join('\n', '<script src="{}"></script>', ((url,) for url in urls))


@hooks.register('insert_editor_js')
def editor_js():
    urls = [
        'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.4/lodash.min.js',
        static('js/admin.js'),
    ]

    return format_html_join('\n', '<script src="{}"></script>', ((url,) for url in urls))


@hooks.register('before_edit_page')
def before_edit_page(request, page):
    print(f'BeforeEditHook request: {request}')
    print(f'BeforeEditHook page: "{page}" of type "{type(page)}"')

    assert request.user.is_authenticated
    print(f'BeforeEditHook {request.user.email} is in groups {[group.name for group in request.user.groups.all()]}')


class LocationModelAdmin(ModelAdmin):
    model = Location
    search_fields = ('street',)


class TopicModelAdmin(ModelAdmin):
    model = Topic
    search_fields = ('text',)


class ContactModelAdmin(ModelAdmin):
    model = Contact


class ReallyAwesomeGroup(ModelAdminGroup):
    # menu_label = 'Important Snippets'
    items = (LocationModelAdmin, TopicModelAdmin, ContactModelAdmin)


modeladmin_register(ReallyAwesomeGroup)
