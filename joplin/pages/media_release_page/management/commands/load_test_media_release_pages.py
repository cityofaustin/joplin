from django.core.management.base import BaseCommand, CommandError
import pages.media_release_page.fixtures as media_release_page_fixtures

'''
    Loads media_release_page fixtures into your joplin environment.

    Run with:
    pipenv run python joplin/manage.py load_test_media_release_pages
'''
class Command(BaseCommand):
    help = "Loads test data for manual exploration of test media_release pages"

    def handle(self, *args, **options):
        media_release_page_fixtures.load_all()
