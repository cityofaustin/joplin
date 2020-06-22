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


# Test that page_status passes through to template
@pytest.mark.django_db
def test_page_status_template():
    page = service_page_fixtures.kitchen_sink()
    page.live = True
    page.published = True
    rendered_template = render_page_status_tag_template(page)
    assert f'<div class="coa-page-status__value-container"><a href="{page.janis_publish_url()}" target="_blank" class="coa-page-status__live-badge">Live</a></div>' == rendered_template

@pytest.mark.django_db
def test_page_status_live():
    page = service_page_fixtures.kitchen_sink()
    page.live = True
    page.published = True
    assert page.status_string == "Live"


@pytest.mark.django_db
def test_page_status_draft():
    page = service_page_fixtures.kitchen_sink()
    page.live = False
    page.published = False
    assert page.status_string == "Draft"


@pytest.mark.django_db
def test_page_status_live_and_publishing():
    page = service_page_fixtures.kitchen_sink()
    page.live = True
    page.published = True
    page.publish_request_enqueued = True
    assert page.status_string == "Live + Publishing"


@pytest.mark.django_db
def test_page_status_publishing():
    page = service_page_fixtures.kitchen_sink()
    page.live = True
    page.published = False
    assert page.status_string == "Publishing"


@pytest.mark.django_db
def test_page_status_live_and_draft():
    page = service_page_fixtures.kitchen_sink()
    page.live = True
    page.published = True
    page.has_unpublished_changes = True
    assert page.status_string == "Live + Draft"


@pytest.mark.django_db
def test_page_status_unpublishing():
    page = service_page_fixtures.kitchen_sink()
    page.live = False
    page.published = True
    assert page.status_string == "Live + Unpublishing"
