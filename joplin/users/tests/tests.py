import pytest
from django.core.exceptions import ValidationError
from users.tests.utils.make_user_form import make_user_form


@pytest.mark.django_db
def test_make_user_without_department():
    user_data = {
      "email": "faker@austintexas.io",
      "first_name": "Fake",
      "last_name": "User",
      "password1": "123",
      "password2": "123",
      "roles": "2",
      "department": ""
    }
    form = make_user_form(user_data)
    is_valid = form.is_valid()
    assert is_valid is False
    assert type(form._errors['department'].data[0]) is ValidationError


@pytest.mark.django_db
def test_make_superuser_without_department():
    user_data = {
      "email": "faker@austintexas.io",
      "first_name": "Fake",
      "last_name": "User",
      "password1": "123",
      "password2": "123",
      "roles": "2",
      "department": "",
      "is_superuser": "on",
    }
    form = make_user_form(user_data)
    is_valid = form.is_valid()
    assert is_valid is True


@pytest.mark.django_db
def test_make_user_without_roles(department):
    user_data = {
      "email": "faker@austintexas.io",
      "first_name": "Fake",
      "last_name": "User",
      "password1": "123",
      "password2": "123",
      "department": department.pk,
    }
    form = make_user_form(user_data)
    is_valid = form.is_valid()
    assert is_valid is False
    assert type(form._errors['roles'].data[0]) is ValidationError


@pytest.mark.django_db
def test_make_superuser_without_roles(department):
    user_data = {
      "email": "faker@austintexas.io",
      "first_name": "Fake",
      "last_name": "User",
      "password1": "123",
      "password2": "123",
      "department": department.pk,
      "is_superuser": "on",
    }
    form = make_user_form(user_data)
    is_valid = form.is_valid()
    assert is_valid is True


@pytest.mark.django_db
def test_make_user_without_roles_or_department():
    user_data = {
      "email": "faker@austintexas.io",
      "first_name": "Fake",
      "last_name": "User",
      "password1": "123",
      "password2": "123",
      "department": "",
    }
    form = make_user_form(user_data)
    is_valid = form.is_valid()
    assert is_valid is False
    assert type(form._errors['department'].data[0]) is ValidationError
    assert type(form._errors['roles'].data[0]) is ValidationError


@pytest.mark.django_db
def test_make_superuser_without_roles_or_department():
    user_data = {
      "email": "faker@austintexas.io",
      "first_name": "Fake",
      "last_name": "User",
      "password1": "123",
      "password2": "123",
      "department": "",
      "is_superuser": "on",
    }
    form = make_user_form(user_data)
    is_valid = form.is_valid()
    assert is_valid is True


@pytest.mark.django_db
def test_make_user_with_roles_and_department(department):
    user_data = {
      "email": "faker@austintexas.io",
      "first_name": "Fake",
      "last_name": "User",
      "password1": "123",
      "password2": "123",
      "roles": "2",
      "department": department.pk,
    }
    form = make_user_form(user_data)
    is_valid = form.is_valid()
    assert is_valid is True


@pytest.mark.django_db
def test_make_superuser_with_roles_and_department(department):
    user_data = {
      "email": "faker@austintexas.io",
      "first_name": "Fake",
      "last_name": "User",
      "password1": "123",
      "password2": "123",
      "roles": "2",
      "department": department.pk,
      "is_superuser": "on",
    }
    form = make_user_form(user_data)
    is_valid = form.is_valid()
    assert is_valid is True


@pytest.mark.django_db
def test_editor_makes_page_under_department(department):
    user_data = {
      "email": "faker@austintexas.io",
      "first_name": "Fake",
      "last_name": "User",
      "password1": "123",
      "password2": "123",
      "roles": "2",
      "department": department.pk,
    }
    pass


@pytest.mark.django_db
def test_editor_cannot_make_departmentless_page():
    pass


@pytest.mark.django_db
def test_admin_can_make_departmentless_page():
    pass


@pytest.mark.django_db
def test_editor_can_make_any_department_page():
    pass
