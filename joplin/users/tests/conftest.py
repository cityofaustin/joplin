import pytest
import groups.fixtures as department_fixtures
import users.fixtures as user_fixtures


@pytest.fixture()
def department():
    return department_fixtures.title()


@pytest.fixture()
def superadmin():
    return user_fixtures.superadmin()


@pytest.fixture()
def editor():
    return user_fixtures.editor_for_test_env()
