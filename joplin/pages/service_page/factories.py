import json
from pages.service_page.models import ServicePage
from pages.topic_page.factories import JanisBasePageWithTopicsFactory


class ServicePageFactory(JanisBasePageWithTopicsFactory):
    @classmethod
    def create(cls, *args, **kwargs):
        # if we have dynamic content
        if 'dynamic_content' in kwargs:
            # convert it into a StreamField-parseable json dump
            formatted_dynamic_content = json.dumps([
                {
                    u'type': u'{0}'.format(dynamic_content_block['type']),
                    u'value': u'{0}'.format(dynamic_content_block['value'])
                }
                for dynamic_content_block in kwargs['dynamic_content']
            ])
            kwargs['dynamic_content'] = formatted_dynamic_content

        # Convert steps into StreamField-parseable json dump
        step_keywords = ['steps', 'steps_es']
        for step_keyword in step_keywords:
            steps = kwargs.pop(step_keyword, [])

            formatted_steps = []
            for step in steps:
                # todo: don't skip these
                if step['type'] == 'step_with_locations':
                    continue

                formatted_step = {'type': u'{0}'.format(step['type'])}
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
