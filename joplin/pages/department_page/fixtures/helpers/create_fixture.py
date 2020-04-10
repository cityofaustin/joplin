from pages.department_page.models import DepartmentPage
from pages.department_page.factories import DepartmentPageFactory


# Skips creating fixture if Page with slug already exists
def create_fixture(page_data, fixture_name):
    try:
        page = DepartmentPage.objects.get(slug=page_data['slug'])
    except DepartmentPage.DoesNotExist:
        page = None
    if page:
        print(f"Skipping {fixture_name}")
        return None

    page = DepartmentPageFactory.create(**page_data)
    print(f"Built {fixture_name}")
    return page
