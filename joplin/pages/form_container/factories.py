from pages.form_container.models import FormContainer
from pages.topic_page.factories import JanisBasePageWithTopicsFactory


class FormContainerFactory(JanisBasePageWithTopicsFactory):
    class Meta:
        model = FormContainer
