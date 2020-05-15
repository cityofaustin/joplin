import pytest

from pages.news_page.models import NewsPage
import pages.news_page.fixtures as fixtures

# For news pages, we need to make sure our urls and our byline departments are set correctly
# example:
# "From Austin Public Health, written by Communications and Public Information Office"

@pytest.mark.django_db
def test_written_by_APH():
    # APH makes a page for APH, doesn’t assign a different department:
    page = fixtures.written_by_APH()

    # Make sure we made a news page
    assert isinstance(page, NewsPage)

    # Make sure we only have one instance
    assert len(page.janis_instances()) == 1
    janis_instance = page.janis_instances()[0]

    # Make sure we only have one URL
    assert len(page.janis_urls()) == 1
    janis_url = page.janis_urls()[0]

    # Make sure the URL is APH
    assert janis_instance['url'] == '/mvp-news-aph/mvp-news-by-aph/'
    assert janis_url == '/mvp-news-aph/mvp-news-by-aph/'

    # Make sure "From" is APH
    assert janis_instance['from_department'].title == 'Austin Public Health'

    # Make sure written by is not shown
    assert not janis_instance['by_department']


@pytest.mark.django_db
def test_written_by_APH_written_for_APH():
    # APH makes a page for APH, doesn’t assign a different department:
    page = fixtures.written_by_APH_written_for_APH()

    # Make sure we made a news page
    assert isinstance(page, NewsPage)

    # Make sure we only have one instance
    assert len(page.janis_instances()) == 1
    janis_instance = page.janis_instances()[0]

    # Make sure we only have one URL
    assert len(page.janis_urls()) == 1
    janis_url = page.janis_urls()[0]

    # Make sure the URL is APH
    assert janis_instance['url'] == '/mvp-news-aph/mvp-news/'
    assert janis_url == '/mvp-news-aph/mvp-news/'

    # Make sure "From" is APH
    assert janis_instance['from_department'].title == 'Austin Public Health'

    # Make sure written by is not shown
    assert not janis_instance['by_department']


@pytest.mark.django_db
def test_written_by_CPIO_written_for_APH():
    # APH makes a page for APH, doesn’t assign a different department:
    page = fixtures.written_by_CPIO_written_for_APH()

    # Make sure we made a news page
    assert isinstance(page, NewsPage)

    # Make sure we only have one instance
    assert len(page.janis_instances()) == 1
    janis_instance = page.janis_instances()[0]

    # Make sure we only have one URL
    assert len(page.janis_urls()) == 1
    janis_url = page.janis_urls()[0]

    # Make sure the URL is APH
    assert janis_instance['url'] == '/mvp-news-aph/mvp-news-by-cpio-for-aph/'
    assert janis_url == '/mvp-news-aph/mvp-news-by-cpio-for-aph/'

    # Make sure "From" is APH
    assert janis_instance['from_department'].title == 'Austin Public Health'

    # Make sure written by is CPIO
    assert janis_instance['by_department'].title == 'Communications and Public Information Office'
