import pytest
from django.core.exceptions import ValidationError
from users.tests.utils.make_user_form import make_user_form
from base.views.new_page_from_modal import new_page_from_modal
from pages.information_page.models import InformationPage
from pages.home_page.factories import HomePageFactory
from base.views.joplin_search_views import dept_explorable_pages
import pages.service_page.fixtures as fixtures
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
    kitchen_sink_service_page = fixtures.kitchen_sink()
    departmentless_page = fixtures.step_with_1_location()
    # explorable_pages = dept_explorable_pages(editor)
    # print('exp ', explorable_pages)
    # assert False

    # from wagtail's test explorable pages
    # event_editor = get_user_model().objects.get(username='eventeditor')
    # christmas_page = EventPage.objects.get(url_path='/home/events/christmas/')
    # unpublished_event_page = EventPage.objects.get(url_path='/home/events/tentative-unpublished-event/')
    # someone_elses_event_page = EventPage.objects.get(url_path='/home/events/someone-elses-event/')
    # about_us_page = Page.objects.get(url_path='/home/about-us/')
    #
    # user_perms = UserPagePermissionsProxy(event_editor)
    # explorable_pages = user_perms.explorable_pages()
    #
    # # Verify all pages below /home/events/ are explorable
    # self.assertTrue(explorable_pages.filter(id=christmas_page.id).exists())
    # self.assertTrue(explorable_pages.filter(id=unpublished_event_page.id).exists())
    # self.assertTrue(explorable_pages.filter(id=someone_elses_event_page.id).exists())
    #
    # # Verify page outside /events/ tree are not explorable
    # self.assertFalse(explorable_pages.filter(id=about_us_page.id).exists())


@pytest.mark.django_db
def test_superadmin_explores_all_pages(superadmin):
    explorable_pages = dept_explorable_pages(superadmin)
    # check that the explorable pages length is the same as all pages?

