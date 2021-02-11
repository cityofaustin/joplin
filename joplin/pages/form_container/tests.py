import pytest
from importer.page_importer import PageImporter
from pages.form_container.models import FormContainer


# @pytest.mark.django_db
@pytest.mark.skip("importer test")
def test_create_form_container_from_api(remote_staging_preview_url, test_api_url, test_api_jwt_token):
    url = f'{remote_staging_preview_url}/form/UGFnZVJldmlzaW9uTm9kZToyOQ==?CMS_API={test_api_url}'
    page = PageImporter(url, test_api_jwt_token).fetch_page_data().create_page()
    assert isinstance(page, FormContainer)
