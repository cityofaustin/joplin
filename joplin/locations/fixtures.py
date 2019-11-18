from locations import factories
from django.conf import settings
from django.core.management import call_command
from pathlib import Path


def create():
    """
    using our factories, lets make some test ObjectList

    FYI: create and create_batch commits to the DB you are running
    build, build_batch does not, which might be preferable generating fixtures
    for the frontend

    BUT: build does not appear to build related objects as is, so we may just
    need to be commit to the database for now and revisit this in a more efficient way later
    """

    def create_fixtures():
        """
        creates test data and commits to DB
        """
        return factories.LocationPageFactory.create_batch(size=10)

    def save_to_file(objects):
        import json
        from django.core.serializers import serialize
        # simple representation of an object
        # relations just have PK, not that data

        with open('fixtures.json', 'w', encoding='utf-8') as output:
            json.dump(serialize('json', objects), output, ensure_ascii=False, indent=4)

    def dump_data():
        """
        uses django managment to dump. in this case we specificy the model/app to it only dumps that data
        """
        path = Path(__file__).parent.absolute()
        # with open('./fixtures.json', 'w') as out:
        call_command('dumpdata', 'locations', '--natural-foreign', output=path.joinpath('fixtures.json'), verbosity=0, indent=4)

    def cleanup():
        """
        deletes the objects made from the db
        this is probably a bad way to do this, we don't want to accidentially delete
        data we care about, right?
        """
        locations.models.LocationPage.objects.all().delete()

    create_fixtures()
    dump_data()
    cleanup()
