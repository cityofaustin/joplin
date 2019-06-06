from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html_join

from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.admin.widgets import Button, ButtonWithDropdownFromHook, PageListingButton
from wagtail.core import hooks

from base.models import HomePage, Location, Contact
from wagtail.core.models import PageRevision

from html.parser import HTMLParser

# Following this: https://docs.python.org/3/library/html.parser.html#examples
class CheckForDataInHTMLParser(HTMLParser):
    has_data = False

    def handle_data(self, data):
        self.has_data = True


@hooks.register('before_edit_page')
def before_edit_page(request, page):
    print(f'BeforeEditHook request: {request}')
    print(f'BeforeEditHook page: "{page}" of type "{type(page)}"')

    assert request.user.is_authenticated
    print(f'BeforeEditHook {request.user.email} is in groups {[group.name for group in request.user.groups.all()]}')


@hooks.register('construct_main_menu')
def configure_main_menu(request, menu_items):
    new_items = []

    contacts_item = MenuItem('', "/admin/snippets/base/contact/", classnames="icon icon-group", order=800)
    new_items.append(contacts_item)

    locations_item = MenuItem('', "/admin/snippets/base/location/", classnames="icon icon-locations", order=900)
    new_items.append(locations_item)

    # @TODO: make sure this only shows for admins
    manage_users_item = MenuItem('', "/admin/users/", classnames="icon icon-group", order=1000)
    new_items.append(manage_users_item)

    for item in menu_items:
        if item.name in ('home', 'images'):
            item.label = ''
            new_items.append(item)
    menu_items[:] = new_items


@hooks.register('register_admin_menu_item')
def register_page_list_menu_item():
    home = HomePage.objects.first()
    return MenuItem('Home', reverse('wagtailadmin_explore', args=[home.pk]), classnames='icon icon-home', order=10)

@hooks.register('register_joplin_page_listing_buttons')
def joplin_page_listing_buttons(page, page_perms, is_parent=False):
    if page_perms.can_edit():
        yield PageListingButton(
            _('Edit'),
            reverse('wagtailadmin_pages:edit', args=[page.id]),
            attrs={'title': _("Edit '{title}'").format(title=page.get_admin_display_title())},
            priority=10
        )
    if page.has_unpublished_changes:
        yield PageListingButton(
            _('View draft'),
            page.janis_preview_url(),
            attrs={'title': _("Preview draft version of '{title}'").format(title=page.get_admin_display_title()), 'target': '_blank'},
            priority=20
        )
    if page.live and page.url and hasattr(page, 'janis_url'):
        yield PageListingButton(
            _('View live'),
            page.janis_url(),
            attrs={'target': "_blank", 'title': _("View live version of '{title}'").format(title=page.get_admin_display_title())},
            priority=30
        )

    # This is kinda hacky but it should let us know when we have notes on a revision
    latest_revision = None
    all_revisions = PageRevision.objects.filter(page_id=page.id)
    for revision in all_revisions:
        if revision.is_latest_revision():
            latest_revision = revision

    if latest_revision:
        author_notes = latest_revision.as_page_object().author_notes

        # Following this: https://docs.python.org/3/library/html.parser.html#examples
        parser = CheckForDataInHTMLParser()
        parser.feed(author_notes)

        if parser.has_data:
            yield Button(
                _('📝'),
                'javascript:alert("Wouldn\'t it be cool if this linked to the notes?");',
                attrs={'title': _("Notes for authors entered"), 'class':'has-author-notes'},
                priority=70
            )

    yield ButtonWithDropdownFromHook(
        _('More'),
        hook_name='register_joplin_page_listing_more_buttons',
        page=page,
        page_perms=page_perms,
        is_parent=is_parent,
        attrs={'target': '_blank', 'title': _("View more options for '{title}'").format(title=page.get_admin_display_title())},
        priority=50
    )


@hooks.register('register_joplin_page_listing_more_buttons')
def joplin_page_listing_more_buttons(page, page_perms, is_parent=False):
    if not page.is_root():
        yield Button(
            _('Copy'),
            reverse('wagtailadmin_pages:copy', args=[page.id]),
            attrs={'title': _("Copy page '{title}'").format(title=page.get_admin_display_title())},
            priority=20
        )
    # if not page.live:
    #     yield Button(
    #         _('Archive'),
    #         "#TODO-archive",
    #         attrs={'title': _("Archive page '{title}'").format(title=page.get_admin_display_title())},
    #         priority=30
    #     )
    if page_perms.can_unpublish():
        yield Button(
            _('Unpublish'),
            reverse('wagtailadmin_pages:unpublish', args=[page.id]),
            attrs={'title': _("Unpublish page '{title}'").format(title=page.get_admin_display_title())},
            priority=40
        )
    if page_perms.can_publish() and page.has_unpublished_changes:
        yield Button(
            _('Publish'),
            reverse('publish', args=[page.id]),
            attrs={'title': _("Publish page '{title}'").format(title=page.get_admin_display_title())},
            priority=50
        )
    if not page.is_root():
        yield Button(
            _('Revisions'),
            reverse('wagtailadmin_pages:revisions_index', args=[page.id]),
            attrs={'title': _("View revision history for '{title}'").format(title=page.get_admin_display_title())},
            priority=60
        )


class LocationModelAdmin(ModelAdmin):
    model = Location
    search_fields = ('street',)


class ContactModelAdmin(ModelAdmin):
    model = Contact

class ReallyAwesomeGroup(ModelAdminGroup):
    menu_label = 'Important Snippets'
    items = (LocationModelAdmin, ContactModelAdmin)


modeladmin_register(ReallyAwesomeGroup)
