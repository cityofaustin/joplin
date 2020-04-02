# Testing

We now have automated tests! They get run on every circleci build during the "test" job. To replicate this process locally:

1. Start a database (`sh scripts/undockered` and quit after postgres starts; dedicated script for database starting is a TODO)
2. run `pipenv run pytest`

## Which tests get run?

Any file that matches the pattern specified in `pytest.ini`.

## How do I make test data?

Test data can be created with factories or by directly creating new instances of your model. Either way works, as long as you can test the thing you want to test.

In the case of publish_preflight tests, we needed to create mock forms to validate against. To create mock forms, we needed to create mock POST requests (called `fake_request`s in code). There is no easy way I've found to automatically make mock POST requests. They were created by setting a breakpoint in pycharm and manually copying the `request.POST` objects from real requests in `wagtail/admin/views/pages.py`.

You can experiment with the test data used in publish_preflight by running `pipenv run python joplin/manage.py load_test_data_publish_preflight` on an empty database (`DROP_DB=on scripts/undockered.py` for now, better empty database creation script to follow). This lets you interact directly with the same pages used to `setUp` the test data for `publish_preflight/tests/test_information_page_publish_preflight.py`. You can create your own new test `fake_request`s to test new criteria.

### Using Factories to make test data in the database

The most basic way would be to:
1. have joplin running,
2. go into the shell like
`pipenv run ./joplin/manage.py shell_plus`
(or just 'shell')
3. Import your factory:
`from locations.factories import LocationPageFactory`
`from base.factories.service_page import ServicePageFactory`
4. `ServicePageFactory.create(parent=HomePage.objects.first())``
or for a bunch
`ServicePageFactory.create_batch(parent=HomePage.objects.first(), size=<integer of how ever many you want to make>)`

## Coverage

Running pytest now also generates coverage reports. You can see this in a console, and also generate a browseable html coverage report.

`pipenv run pytest`

 After that is done:

 `pipenv run pytest coverage html`

 Browse to 'htmlcov' folder and open index.html. Ta-da!

 This coverage report currently dosen't cover templates, and therefore it dosen't cover customizations we've made to the admin (FWIW our test coverage apparently drops down to around 9% if we include Django templates generally, so we'd probably need to narrow our focus to get something useful).

 It also dosen't cover(to my knowledge), test coverage of Javascript code we've written to customize interactions, so keep that in mind.

 Coverage percentage isn't an end-all be-all measure of testability (we could, for instance, write bad tests that still cover the code), and we don't need to shoot for 100% coverage, but it is a helpful objetive indicator of where to start writing tests. It also plainly shows the values of using existing Django functionality or other libraries that have their own tests already.

 We can also mark some files or lines of code as safe to exclude from coverage.

## How do I debug tests?

There is a pycharm runConfiguration included to help you debug tests called [Run_tests](./.idea/runConfigurations/Run_tests.xml).
