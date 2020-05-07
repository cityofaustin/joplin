import pytest

from pages.news_page.models import NewsPage
import pages.service_page.fixtures as fixtures


@pytest.mark.django_db
def test_written_by_APH():
    # APH makes a page for APH, doesn’t assign a different department:
    page = fixtures.written_by_APH()

    #   url is APH
    #   From is APH
    #   Written by is not shown
    assert isinstance(page, NewsPage)
    assert False


@pytest.mark.django_db
def test_written_by_APH_written_for_APH():
    # APH makes a page for APH, picks APH
    page = fixtures.written_by_APH_written_for_APH()

    #   url is APH
    #   From is APH
    #   Written by is not shown
    assert isinstance(page, NewsPage)
    assert False


@pytest.mark.django_db
def test_written_by_CPIO_written_for_APH():
    # CPIO makes a page for APH, picks APH
    page = fixtures.written_by_CPIO_written_for_APH()

    #   url is APH
    #   From is APH
    #   Written by is CPIO
    assert isinstance(page, NewsPage)
    assert False
