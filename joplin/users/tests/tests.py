import pytest
from django.core.exceptions import ValidationError
from users.tests.utils.make_user_form import make_user_form
from pages.information_page.models import InformationPage
from base.views.new_page_from_modal import new_page_from_modal


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
def test_editor_makes_page_under_department(editor, rf):
    # editor creates page
    body = {
            "type": "information",
            "jwtToken": "",
            "title": "Test Page",
            "topic": "",
            "department": "",
    }
    request = rf.post('admin/pages/new_from_modal', body, content_type='application/json')
    request.user = editor

    response = new_page_from_modal(request)
    assert response.status_code is 200
    page_pk = response.content["id"]
    print(page_pk)
    # assert page has a department
    created_page = InformationPage.objects.get(id=page_pk)
   # assert created_page.departments()[0].department is editor.groups


@pytest.mark.django_db
def test_editor_cannot_make_departmentless_page():
    pass


@pytest.mark.django_db
def test_admin_can_make_departmentless_page(superadmin, rf):
    body = {
        "type": "information",
        "jwtToken": "",
        "title": "Test Page",
        "topic": "",
        "department": "",
    }
    request = rf.post('admin/pages/new_from_modal', body, content_type='application/json')
    request.user = superadmin

    response = new_page_from_modal(request)
    assert response.status_code is 200
    page_pk = response.content["id"]
    print(page_pk)
    # assert page has no department
    created_page = InformationPage.objects.get(id=page_pk)
    # assert created_page.departments()[0].department is editor.groups


@pytest.mark.django_db
def test_editor_can_make_any_department_page():
    pass
