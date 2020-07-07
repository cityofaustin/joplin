from django.core.management.base import BaseCommand, CommandError
from pages.official_documents_collection.models import OfficialDocumentCollection


def remove_copy_from_slugs():
    """

    :return:
    """
    official_document_collection = OfficialDocumentCollection.objects.all()

    for collection in official_document_collection.iterator():
        old_slug = collection.slug
        collection.slug = old_slug[:-5] # removing '-copy'
        collection.save()


class Command(BaseCommand):
    help = "Copies data from Official Document Pages to Official Document Collections "

    def handle(self, *args, **options):
        remove_copy_from_slugs()

