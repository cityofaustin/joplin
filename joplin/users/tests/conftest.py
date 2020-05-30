import pytest
import groups.fixtures as department_fixtures
import users.fixtures as user_fixtures
import pages.service_page.fixtures as service_fixtures


@pytest.fixture()
def department():
    return department_fixtures.title()


@pytest.fixture()
def superadmin():
    return user_fixtures.superadmin()


@pytest.fixture()
def editor():
    return user_fixtures.editor_for_test_env()


@pytest.fixture()
def kitchen_service():
    return service_fixtures.kitchen_sink()


@pytest.fixture()
def departmentless_service():
    return service_fixtures.step_with_1_location()
