from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html_join

from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.admin.widgets import Button, ButtonWithDropdownFromHook, PageListingButton
from wagtail.core import hooks

from base.models import HomePage, Topic, Location, Contact
import os
import graphene

@hooks.register('before_edit_page')
def before_edit_page(request, page):
    print(f'BeforeEditHook request: {request}')
    print(f'BeforeEditHook page: "{page}" of type "{type(page)}"')

    assert request.user.is_authenticated
    print(f'BeforeEditHook {request.user.email} is in groups {[group.name for group in request.user.groups.all()]}')


@hooks.register('construct_main_menu')
def configure_main_menu(request, menu_items):
    new_items = []
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
        revision = page.get_latest_revision()

        page_type = type(revision.page).__name__

        # TODO: Add other page types
        if "Service" in page_type:
          url_page_type = "services"

        if "Process" in page_type:
          url_page_type = "processes"

        global_id = graphene.Node.to_global_id('PageRevisionNode', revision.id)

        yield PageListingButton(
            _('View draft'),
            os.environ["JANIS_URL"] + "/en/preview/" + url_page_type + "/" + global_id,
            attrs={'title': _("Preview draft version of '{title}'").format(title=page.get_admin_display_title()), 'target': '_blank'},
            priority=20
        )
    if page.live and page.url:
        page_type = type(page).__name__
        page_slug = page.slug

        # TODO: Add other page types
        if "Service" in page_type:
          url_page_type = "services"

        if "Process" in page_type:
          url_page_type = "processes"

        yield PageListingButton(
            _('View live'),
            os.environ["JANIS_URL"] + "/en/" + url_page_type + "/" + page_slug,
            attrs={'target': "_blank", 'title': _("View live version of '{title}'").format(title=page.get_admin_display_title())},
            priority=30
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
    if page_perms.can_delete():
        yield Button(
            _('Delete'),
            reverse('wagtailadmin_pages:delete', args=[page.id]),
            attrs={'title': _("Delete page '{title}'").format(title=page.get_admin_display_title())},
            priority=30
        )
    if page_perms.can_unpublish():
        yield Button(
            _('Unpublish'),
            reverse('wagtailadmin_pages:unpublish', args=[page.id]),
            attrs={'title': _("Unpublish page '{title}'").format(title=page.get_admin_display_title())},
            priority=40
        )
    if not page.is_root():
        yield Button(
            _('Revisions'),
            reverse('wagtailadmin_pages:revisions_index', args=[page.id]),
            attrs={'title': _("View revision history for '{title}'").format(title=page.get_admin_display_title())},
            priority=50
        )


class LocationModelAdmin(ModelAdmin):
    model = Location
    search_fields = ('street',)


class TopicModelAdmin(ModelAdmin):
    model = Topic
    search_fields = ('text',)


class ContactModelAdmin(ModelAdmin):
    model = Contact


class ReallyAwesomeGroup(ModelAdminGroup):
    menu_label = 'Important Snippets'
    items = (LocationModelAdmin, TopicModelAdmin, ContactModelAdmin)


modeladmin_register(ReallyAwesomeGroup)
