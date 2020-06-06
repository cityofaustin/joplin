from pages.service_page.models import ServicePage
from pages.topic_page.factories import JanisBasePageWithTopicsFactory
from pages.base_page.fixtures.helpers.streamfieldify import streamfieldify


class ServicePageFactory(JanisBasePageWithTopicsFactory):
    @classmethod
    def create(cls, *args, **kwargs):
        if 'dynamic_content' in kwargs:
            kwargs['dynamic_content'] = streamfieldify(kwargs['dynamic_content'])

        step_keywords = ['steps', 'steps_es']
        for step_keyword in step_keywords:
            if step_keyword in kwargs:
                kwargs[step_keyword] = streamfieldify(kwargs[step_keyword])

        return super(ServicePageFactory, cls).create(*args, **kwargs)

    class Meta:
        model = ServicePage
