# Testing

We now have automated tests! They get run on every circleci build during the "test" job. To replicate this process locally:

1. Start a database (`sh scripts/undockered` and quit after postgres starts; dedicated script for database starting is a TODO)
2. run `pipenv run pytest`

## Which tests get run?

Any file that matches the pattern specified in `pytest.ini`.

## How do I make test data?

Test data can be created with factories or by directly creating new instances of your model. Either way works, as long as you can test the thing you want to test.

In the case of publish_preflight tests, we needed to create mock forms to validate against. To create mock forms, we needed to create mock POST requests (called `fake_request`s in code). There is no easy way I've found to automatically make mock POST requests. They were created by setting a breakpoint in pycharm and manually copying the `request.POST` objects from real requests.

You can experiment with the test data used in publish_preflight by running `pipenv run python joplin/manage.py load_test_data_publish_preflight` on an empty database (`DROP_DB=on scripts/undockered.py` for now, better empty database creation script to follow). This lets you interact directly with the same pages used to `setUp` the test data for `publish_preflight/tests/test_information_page_publish_preflight.py`. You can create your own new test `fake_request`s to test new criteria.

## How do I debug tests?

There is a pycharm runConfiguration included to help you debug tests called [Run_tests](./.idea/runConfigurations/Run_tests.xml).
