import json
from pages.service_page.models import ServicePage
from pages.topic_page.factories import JanisBasePageWithTopicsFactory


class ServicePageFactory(JanisBasePageWithTopicsFactory):
    @classmethod
    def create(cls, *args, **kwargs):
        # Convert steps into StreamField-parseable json dump
        step_keywords = ['steps', 'steps_es']
        for step_keyword in step_keywords:
            steps = kwargs.pop(step_keyword, [])

            steps_to_format = []
            for step in steps:
                step_to_format = {'type': step['type']}
                if step['type'] == 'step_with_options_accordian':
                    blarg = step['value']['options']

                    blargacious = json.dumps([
                        {
                            u'option_name': u'{0}'.format(option['option_name']),
                            u'option_description': u'{0}'.format(option['option_description'])
                        }
                        for option in blarg
                    ])

                    step_to_format['value'] = {
                        'options_description': step['value']['options_description'],
                        'options': blargacious
                    }
                else:
                    step_to_format['value'] = step['value']
                steps_to_format.append(step_to_format)

            formatted_steps = json.dumps([
                {
                    u'type': u'{0}'.format(step['type']),
                    u'value': u'{0}'.format(step['value'])
                }
                for step in steps_to_format
            ])
            kwargs[step_keyword] = formatted_steps
        return super(ServicePageFactory, cls).create(*args, **kwargs)


    class Meta:
        model = ServicePage
