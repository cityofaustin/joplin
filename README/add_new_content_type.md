## Creating a new page model

TODO.

## Importer

Importer imports from preview urls, so we use the model's `janis_url_page_type` as the key within `importer/queries.py` and `pages/base_page/fixtures/helpers/page_type_map.py`.

1. Add a query to get revision for your page_type in `importer/queries.py`.
  - Test that you have what you wanted by running `pipenv run python joplin/importer/queries.py your_page_type`.
2. Add your page_type's model and factory to `pages/base_page/fixtures/helpers/page_type_map.py`.
  - The create_fixture function in `pages/base_page/fixtures/helpers/create_fixture_map.py` will be automatically created for you.
3. Make a test case within `importer/tests.py` or `pages/your_page_type/tests.py` to ensure that importing works as expected.
