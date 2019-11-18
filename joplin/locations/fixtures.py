from base.models import HomePage
from pathlib import Path
from django.core.management import call_command
from django.conf import settings
from locations import factories


def create():
    """
    using our factories, lets make some test ObjectList

    FYI: create and create_batch commits to the DB you are running
    build, build_batch does not, which might be preferable generating fixtures
    for the frontend

    BUT: build does not appear to build related objects as is, so we may just
    need to be commit to the database for now and revisit this in a more efficient way later
    """
    home_page = HomePage.objects.all()[0]

    def create_fixtures():
        """
        creates test data and commits to DB
        """
        create_index_page = factories.LocationsIndexPageFactory.create(parent=home_page)
        create_locations_pages = factories.LocationPageFactory.create_batch(size=10, parent=create_index_page)

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
        call_command('dumpdata', 'locations.LocationPage', output=path.joinpath('fixture_data.json'), verbosity=0, indent=4)

    def cleanup():
        """
        deletes the objects made from the db
        this is probably a bad way to do this, we don't want to accidentially delete
        data we care about, right?
        """
        try:
            import locations
            locations.models.LocationPage.objects.all().delete()
        except Exception as e:
            print(e)
            import pdb
            pdb.set_trace()

    create_fixtures()
    dump_data()
    # cleanup()
