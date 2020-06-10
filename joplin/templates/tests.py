import pytest
from django.template import Context, Template

import pages.service_page.fixtures as information_page_fixtures


def render_page_status_tag_template(page):
    context = Context({'page': page})
    template_to_render = Template(
        '{% include "wagtailadmin/shared/page_status_tag.html" with page=page %}'
    )
    rendered_template = template_to_render.render(context).strip()
    return rendered_template


@pytest.mark.django_db
def test_page_status_tag_live(expected_publish_url_base):
    page = information_page_fixtures.kitchen_sink()
    rendered_template = render_page_status_tag_template(page)
    assert f'<a href="{expected_publish_url_base}/kitchen-sink-department/kitchen-sink-service-page/" target="_blank" class="underlined">Live</a>' == rendered_template


@pytest.mark.django_db
def test_page_status_tag_draft(expected_preview_url_missing_revision):
    page = information_page_fixtures.new_contact()
    rendered_template = render_page_status_tag_template(page)
    assert f'<a href="{expected_preview_url_missing_revision}" class="underlined">Draft</a>' == rendered_template
