from django.core.management.base import BaseCommand, CommandError
import pages.official_documents_collection.fixtures as official_documents_collection_fixtures


class Command(BaseCommand):
    """
        Loads official document collection page fixtures into your joplin environment.

        Run with:
        pipenv run python joplin/manage.py load_test_official_documents_collection
    """
    help = "Loads test data for manual exploration of test topic pages"

    def handle(self, *args, **options):
        official_documents_collection_fixtures.load_all()
