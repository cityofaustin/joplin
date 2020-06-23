from django.core.management.base import BaseCommand
import pages.official_documents_collection.fixtures as official_documents_collection_fixtures


class Command(BaseCommand):
    """
        Loads topic page fixtures into your joplin environment.

        Run with:
        pipenv run python joplin/manage.py load_test_topic_pages
    """
    help = "Loads test data for manual exploration of test topic pages"

    def handle(self, *args, **options):
        official_documents_collection_fixtures.load_all()
