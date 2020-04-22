import pytest
import groups.fixtures as department_fixtures


@pytest.fixture()
def department():
    return department_fixtures.title()
