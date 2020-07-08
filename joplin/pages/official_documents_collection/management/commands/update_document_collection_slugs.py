from django.core.management.base import BaseCommand, CommandError
from pages.official_documents_collection.models import OfficialDocumentCollection


def remove_copy_from_slugs():
    """
    Iterates through official document collection and removes the last 5 characters from the slug
    Should only be used after copying old official document pages to collections
    """
    official_document_collection = OfficialDocumentCollection.objects.all()

    for collection in official_document_collection.iterator():
        old_slug = collection.slug
        collection.slug = old_slug[:-5]  # removing '-copy'
        collection.save()


class Command(BaseCommand):
    help = "Removes temporary -copy string used as placeholder while copying data"

    def handle(self, *args, **options):
        remove_copy_from_slugs()
