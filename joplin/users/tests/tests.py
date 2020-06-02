import pytest
import os
from django.core.exceptions import ValidationError
from django.test import Client
from django.urls import reverse
from django.contrib import auth
from users.tests.utils.make_user_form import make_user_form
from base.views.new_page_from_modal import new_page_from_modal
from pages.information_page.models import InformationPage
from pages.home_page.factories import HomePageFactory
from base.views.joplin_search_views import dept_explorable_pages
import pages.service_page.fixtures as service_fixtures
import json


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
    page_data = {
        "publish_janis_branch_for_pr": "pytest",
        "preview_janis_branch_for_pr": "pytest",
        "slug": "pytest",
        "title": "pytest",
    }
    HomePageFactory.create(**page_data)
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

    # assert page is created
    response = new_page_from_modal(request)
    assert response.status_code is 200
    # assert page has a department that matches editor department
    response_json = json.loads(response.content.decode('utf-8'))
    page_pk = response_json['id']
    created_page = InformationPage.objects.get(id=page_pk)
    editor_department = editor.groups.get(name="Kitchen sink department")
    assert created_page.departments()[0].department.pk is editor_department.department.pk


@pytest.mark.django_db
def test_admin_can_make_departmentless_page(superadmin, rf):
    page_data = {
        "publish_janis_branch_for_pr": "pytest",
        "preview_janis_branch_for_pr": "pytest",
        "slug": "pytest",
        "title": "pytest",
    }
    HomePageFactory.create(**page_data)
    body = {
        "type": "information",
        "jwtToken": "",
        "title": "Test Page",
        "topic": "",
        "department": "",
    }
    request = rf.post('admin/pages/new_from_modal', body, content_type='application/json')
    request.user = superadmin

    # assert page is created
    response = new_page_from_modal(request)
    assert response.status_code is 200
    # assert page has a department that matches editor department
    response_json = json.loads(response.content.decode('utf-8'))
    page_pk = response_json['id']
    created_page = InformationPage.objects.get(id=page_pk)
    assert len(created_page.departments()) is 0


@pytest.mark.django_db
def test_editor_cannot_explore_other_dept_pages(editor):
    kitchen_service = service_fixtures.kitchen_sink()
    departmentless_service = service_fixtures.step_with_1_location()
    explorable_pages = dept_explorable_pages(editor)
    # assert that the service page under kitchen sink department is in the results of the kitchen sink editor
    assert explorable_pages.filter(id=kitchen_service.id).exists()
    # assert the page with no department does not show up in the results
    assert not explorable_pages.filter(id=departmentless_service.id).exists()


@pytest.mark.django_db
def test_superadmin_explores_all_pages(superadmin):
    kitchen_service = service_fixtures.kitchen_sink()
    departmentless_service = service_fixtures.step_with_1_location()
    explorable_pages = dept_explorable_pages(superadmin)
    # assert superadmins can explore all pages, regardless of department
    assert explorable_pages.filter(id=kitchen_service.id).exists()
    assert explorable_pages.filter(id=departmentless_service.id).exists()


@pytest.mark.django_db
def test_editor_cant_view_page_without_permission(editor):
    kitchen_service = service_fixtures.kitchen_sink()
    departmentless_service = service_fixtures.step_with_1_location()
    c = Client()
    k_url = reverse('wagtailadmin_pages:edit', args=[kitchen_service.pk])
    print(k_url)
    c.login(username=editor.email, password=os.getenv("API_TEST_USER_PASSWORD"))
    user = auth.get_user(c)
    print(user.get_all_permissions())
    response_allowed = c.get(f'/admin/pages/{kitchen_service.id}/edit/#tab-content')
    print(response_allowed)
    response_forbidden = c.get(f'/admin/pages/{departmentless_service.id}/edit/')
    print(response_forbidden)
    assert False
    #admin/pages/12/edit/#tab-content
# test that someone from the other department cant view the departmentless page
# that it doesnt return 200?
#https://github.com/wagtail/wagtail/blob/882f8f3cf8ddd79c30e611a48882b309e90dad0c/wagtail/admin/tests/test_privacy.py
