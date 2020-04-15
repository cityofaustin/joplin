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
                elif step['type'] == 'step_with_locations':
                    formatted_step['value'] = {
                        'locations': [
                            {
                                'location_page': {
                                # #
                                #     {'location_page': {'id': 'TG9jYXRpb25QYWdlTm9kZTozMjc=',
                                #                        'slug': 'recycle-reuse-drop-off-center',
                                #                        'title': 'Recycle & Reuse Drop-off Center',
                                #                        'physical_street': '2514 Business Center Drive',
                                #                        'physical_unit': '', 'physical_city': 'Austin',
                                #                        'physical_state': 'TX', 'physical_zip': '78744'}}]},
                                # #
                                    u'id': u'{0}'.format(location['location_page']['id']),
                                    u'slug': u'{0}'.format(location['location_page']['slug']),
                                    u'title': u'{0}'.format(location['location_page']['title']),
                                    u'physical_street': u'{0}'.format(location['location_page']['physical_street']),
                                    u'physical_unit': u'{0}'.format(location['location_page']['physical_unit']),
                                    u'physical_city': u'{0}'.format(location['location_page']['physical_city']),
                                    u'physical_state': u'{0}'.format(location['location_page']['physical_state']),
                                    u'physical_zip': u'{0}'.format(location['location_page']['physical_zip']),
                                }
                            }
                            for location in step['value']['locations']
                        ],
                        u'locations_description': u'{0}'.format(step['value']['locations_description']),
                    }
                    pass
                else:
                    formatted_step['value'] = u'{0}'.format(step['value'])
                formatted_steps.append(formatted_step)

            json_steps = json.dumps(formatted_steps)
            kwargs[step_keyword] = json_steps
        return super(ServicePageFactory, cls).create(*args, **kwargs)


    class Meta:
        model = ServicePage
