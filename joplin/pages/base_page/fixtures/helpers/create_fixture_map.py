from pages.base_page.fixtures.helpers.page_type_map import page_type_map


def build_create_fixture(page_type):
    model = page_type_map[page_type]["model"]
    factory = page_type_map[page_type]["factory"]

    '''
        Skips creating fixture if Page with slug already exists.
        **kwargs:
        overrides - A dictionary that contains override values for preset fixtures.
    '''
    def create_fixture(page_data, fixture_name, **kwargs):
        # Override values in fixtures
        overrides = kwargs.pop("overrides", None)
        if overrides:
            for field, value in overrides:
                page_data["field"] = value

        try:
            page = model.objects.get(slug=page_data['slug'])
        except model.DoesNotExist:
            page = None
        if page:
            print(f"Skipping {fixture_name}")
            return None

        page = factory.create(**page_data)
        print(f"Built {fixture_name}")
        return page

    return create_fixture

'''
    Makes an object called "create_fixture_map".
    Contains the create_fixture function for every page_type in page_type_map.

    Example usage:
    from pages.base_page.fixtures.helpers.create_fixture_map import create_fixture_map
    create_fixture = create_fixture_map["information"]
    create_fixture(information_page_data, "my_fixture_name", **kwargs)
'''
create_fixture_map = {}
for page_type in page_type_map:
    create_fixture_map[page_type] = build_create_fixture(page_type)
