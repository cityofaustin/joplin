import json
from pages.service_page.models import ServicePage
from pages.topic_page.factories import JanisBasePageWithTopicsFactory
from pages.base_page.fixtures.helpers.streamfieldify import streamfieldify


class ServicePageFactory(JanisBasePageWithTopicsFactory):
    @classmethod
    def create(cls, *args, **kwargs):
        # if we have dynamic content
        if 'dynamic_content' in kwargs:
            # convert it into a StreamField-parseable json dump
            kwargs['dynamic_content'] = streamfieldify(kwargs['dynamic_content'])

        # Convert steps into StreamField-parseable json dump
        step_keywords = ['steps', 'steps_es']
        for step_keyword in step_keywords:
            # if step_keyword in kwargs:
            #     kwargs[step_keyword] = streamfieldify(kwargs[step_keyword])
            steps = kwargs.pop(step_keyword, [])

            formatted_steps = []
            for step in steps:
                # todo: don't skip these
                formatted_step = {'type': u'{0}'.format(step['type'])}

                if step['type'] == 'step_with_locations':
                    formatted_step = streamfieldify(step)

                if step['type'] == 'step_with_options_accordian':
                    formatted_step['value'] = {
                        'options': [
                            {
                                u'option_description': u'{0}'.format(option['option_description']),
                                u'option_name': u'{0}'.format(option['option_name'])
                            }
                            for option in step['value']['options']
                        ],
                        u'options_description': u'{0}'.format(step['value']['options_description']),
                    }
                else:
                    formatted_step['value'] = u'{0}'.format(step['value'])
                formatted_steps.append(formatted_step)

            json_steps = json.dumps(formatted_steps)
            kwargs[step_keyword] = json_steps
        return super(ServicePageFactory, cls).create(*args, **kwargs)


    class Meta:
        model = ServicePage
