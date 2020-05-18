from django.core.management.base import BaseCommand, CommandError
import pages.news_page.fixtures as news_page_fixtures

'''
    Loads news page fixtures into your joplin environment.

    Run with:
    pipenv run python joplin/manage.py load_test_news_pages
'''
class Command(BaseCommand):
    help = "Loads test data for manual exploration of test news pages"

    def handle(self, *args, **options):
        news_page_fixtures.load_all()
