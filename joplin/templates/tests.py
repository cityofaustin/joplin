import pytest
import re
from django.template import Context, Template

import pages.service_page.fixtures as service_page_fixtures


def render_page_status_tag_template(page):
    context = Context({'page': page})
    template_to_render = Template(
        '{% include "wagtailadmin/shared/page_status_tag.html" with page=page %}'
    )
    rendered_template = template_to_render.render(context)
    # Remove comments
    rendered_template = re.sub("(<!--.*?-->)", "", rendered_template, flags=re.MULTILINE).strip()
    return rendered_template


@pytest.mark.django_db
def test_page_status_live():
    page = service_page_fixtures.kitchen_sink()
    page.live = True
    page.published = True
    rendered_template = render_page_status_tag_template(page)
    assert f'<a href="{page.janis_publish_url()}" target="_blank" class="underlined">Live</a>' == rendered_template


@pytest.mark.django_db
def test_page_status_draft():
    page = service_page_fixtures.kitchen_sink()
    page.live = False
    rendered_template = render_page_status_tag_template(page)
    assert f'<a href="{page.janis_preview_url()}" class="underlined">Draft</a>' == rendered_template


@pytest.mark.django_db
def test_page_status_live_and_updating():
    page = service_page_fixtures.kitchen_sink()
    page.live = True
    page.published = True
    page.publish_request_enqueued = True
    rendered_template = render_page_status_tag_template(page)
    assert f'<div class="coa-header__page-status-value"><a href="{page.janis_publish_url()}" target="_blank" class="underlined">Live</a> + Publishing</div>' == rendered_template


@pytest.mark.django_db
def test_page_status_live_and_publishing_for_first_time():
    page = service_page_fixtures.kitchen_sink()
    page.live = True
    page.published = False
    rendered_template = render_page_status_tag_template(page)
    assert f'<div class="coa-header__page-status-value"><a href="{page.janis_publish_url()}" target="_blank" class="underlined">Live</a> + Publishing</div>' == rendered_template


@pytest.mark.django_db
def test_page_status_live_and_draft():
    page = service_page_fixtures.kitchen_sink()
    page.live = True
    page.published = True
    page.has_unpublished_changes = True
    rendered_template = render_page_status_tag_template(page)
    assert f'<div class="coa-header__page-status-value"><a href="{page.janis_publish_url()}" target="_blank" class="underlined">Live</a> + <a href="{page.janis_preview_url()}" class="underlined">Draft</a></div>' == rendered_template


@pytest.mark.django_db
def test_page_status_unpublishing():
    page = service_page_fixtures.kitchen_sink()
    page.live = False
    page.published = True
    page.has_unpublished_changes = True
    rendered_template = render_page_status_tag_template(page)
    assert f'<div class="coa-header__page-status-value"><a href="{page.janis_publish_url()}" target="_blank" class="underlined">Live</a> + Unpublishing</div>' == rendered_template
