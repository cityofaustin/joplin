import pytest
from importer.page_importer import PageImporter
from django.core.exceptions import ValidationError


def test_parse_janis_preview_url(remote_pytest_preview_url, remote_pytest_api):
    preview_url = f'{remote_pytest_preview_url}/information/UGFnZVJldmlzaW9uTm9kZToyNjI4'

    page_importer = PageImporter(preview_url)

    assert page_importer.joplin_api_endpoint == remote_pytest_api
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'information'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToyNjI4'


def test_parse_unregistered_preview_url():
    preview_url = f'http://fake.base.url/en/preview/information/UGFnZVJldmlzaW9uTm9kZToyNjI4'

    pytest.raises(ValidationError, PageImporter, preview_url)


def test_parse_unregistered_preview_url_with_valid_CMS_API(remote_pytest_api):
    preview_url = f'http://fake.base.url/en/preview/information/UGFnZVJldmlzaW9uTm9kZToyNjI4?CMS_API={remote_pytest_api}'

    page_importer = PageImporter(preview_url)

    assert page_importer.joplin_api_endpoint == remote_pytest_api
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'information'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToyNjI4'


def test_parse_topic_page_dummy_data_janis_preview_url(remote_staging_preview_url, remote_pytest_api):
    preview_url = f'{remote_staging_preview_url}/topic/UGFnZVJldmlzaW9uTm9kZToxMg==?CMS_API={remote_pytest_api}'

    page_importer = PageImporter(preview_url)

    assert page_importer.joplin_api_endpoint == remote_pytest_api
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'topic'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToxMg=='


def test_parse_topic_collection_page_dummy_data_janis_preview_url(remote_staging_preview_url, remote_pytest_api):
    preview_url = f'{remote_staging_preview_url}/topiccollection/UGFnZVJldmlzaW9uTm9kZToxMw==?CMS_API={remote_pytest_api}'

    page_importer = PageImporter(preview_url)

    assert page_importer.joplin_api_endpoint == remote_pytest_api
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'topiccollection'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToxMw=='


def test_parse_information_page_dummy_data_janis_preview_url(remote_staging_preview_url, remote_pytest_api):
    preview_url = f'{remote_staging_preview_url}/information/UGFnZVJldmlzaW9uTm9kZToxMQ==?CMS_API={remote_pytest_api}'

    page_importer = PageImporter(preview_url)

    assert page_importer.joplin_api_endpoint == remote_pytest_api
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'information'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToxMQ=='


def test_parse_service_page_dummy_data_janis_preview_url(remote_staging_preview_url, remote_pytest_api):
    preview_url = f'{remote_staging_preview_url}/services/UGFnZVJldmlzaW9uTm9kZTozNDQ4?CMS_API={remote_pytest_api}'

    page_importer = PageImporter(preview_url)

    assert page_importer.joplin_api_endpoint == remote_pytest_api
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'services'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZTozNDQ4'


def test_parse_location_page_dummy_data_janis_preview_url(remote_staging_preview_url, remote_pytest_api):
    preview_url = f'{remote_staging_preview_url}/location/UGFnZVJldmlzaW9uTm9kZToyMw==?CMS_API={remote_pytest_api}'

    page_importer = PageImporter(preview_url)

    assert page_importer.joplin_api_endpoint == remote_pytest_api
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'location'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToyMw=='


# this test will start breaking once we no longer have this revision in the db
# todo: figure out a good way to mock api responses
# https://docs.python.org/3/library/unittest.mock.html
# @patch('module.ClassName2')
def test_get_dummy_topic_collection_page_from_revision(remote_staging_preview_url, remote_pytest_api):
    preview_url = f'{remote_staging_preview_url}/topiccollection/UGFnZVJldmlzaW9uTm9kZToxMw==?CMS_API={remote_pytest_api}'

    page_dictionaries = PageImporter(preview_url).fetch_page_data().page_dictionaries

    assert page_dictionaries['en']['title'] == 'topic collection title [en]'
    assert page_dictionaries['en']['slug'] == 'topic-collection-title-en'
    assert page_dictionaries['en']['description'] == 'topic collection description [en]'

    # adding themes as a part of our topic collection query
    # instead of importing/testing them separately
    assert page_dictionaries['en']['theme'] == {
        'slug': 'theme-slug-en',
        'text': 'theme text [en]',
        'description': 'theme description [en]'
    }

# this test will start breaking once we no longer have this revision in the db
# todo: figure out a good way to mock api responses
# https://docs.python.org/3/library/unittest.mock.html
# @patch('module.ClassName2')
def test_get_dummy_topic_page_from_revision(remote_staging_preview_url, remote_pytest_api):
    preview_url = f'{remote_staging_preview_url}/topic/UGFnZVJldmlzaW9uTm9kZToxMg==?CMS_API={remote_pytest_api}'

    page_dictionaries = PageImporter(preview_url).fetch_page_data().page_dictionaries

    assert page_dictionaries['en']['title'] == 'topic title [en]'
    assert page_dictionaries['en']['slug'] == 'topic-title-en'
    assert page_dictionaries['en']['description'] == 'topic description [en]'
    assert page_dictionaries['en']['topiccollections'] == {
        'edges': [{
            'node': {
                'topiccollection': {
                    'title': 'topic collection title [en]',
                    'slug': 'topic-collection-title-en',
                    'description': 'topic collection description [en]',
                    'theme': {
                        'slug': 'theme-slug-en',
                        'text': 'theme text [en]',
                        'description': 'theme description [en]'
                    },
                    'live_revision': {
                        'id': 'UGFnZVJldmlzaW9uTm9kZToz'
                    }
                }
            }
        }]
    }


# this test will start breaking once we no longer have this revision in the db
# todo: figure out a good way to mock api responses
# https://docs.python.org/3/library/unittest.mock.html
# @patch('module.ClassName2')
def test_get_dummy_information_page_from_revision(remote_staging_preview_url, remote_pytest_api):
    preview_url = f'{remote_staging_preview_url}/information/UGFnZVJldmlzaW9uTm9kZToxMQ==?CMS_API={remote_pytest_api}'

    page_dictionaries = PageImporter(preview_url).fetch_page_data().page_dictionaries

    assert page_dictionaries['en']['title'] == 'information page title [en]'
    assert page_dictionaries['en']['slug'] == 'information-page-title-en'
    assert page_dictionaries['en']['description'] == 'information page description [en]'
    assert page_dictionaries['en']['topics'] == {
        'edges': [{
            'node': {
                'topic': {
                    'title': 'topic title [en]',
                    'slug': 'topic-title-en',
                    'description': 'topic description [en]',
                    'topiccollections': {
                        'edges': [{
                            'node': {
                                'topiccollection': {
                                    'title': 'topic collection title [en]',
                                    'slug': 'topic-collection-title-en',
                                    'description': 'topic collection description [en]',
                                    'theme': {
                                        'slug': 'theme-slug-en',
                                        'text': 'theme text [en]',
                                        'description': 'theme description [en]'
                                    },
                                    'live_revision': {
                                        'id': 'UGFnZVJldmlzaW9uTm9kZToz'
                                    }
                                }
                            }
                        }]
                    },
                    'live_revision': {
                        'id': 'UGFnZVJldmlzaW9uTm9kZToxMg=='
                    }
                }
            }
        }]
    }
    assert page_dictionaries['en']['additional_content'] == '<p>information page additional content [en]</p>'
    #     todo contacts
    assert not page_dictionaries['en']['coa_global']


def test_get_dummy_service_page_from_revision(remote_staging_preview_url, remote_pytest_api):
    preview_url = f'{remote_staging_preview_url}/services/UGFnZVJldmlzaW9uTm9kZToyMQ==?CMS_API={remote_pytest_api}'

    page_dictionaries = PageImporter(preview_url).fetch_page_data().page_dictionaries
    assert page_dictionaries['en']['title'] == 'Get your bulk items collected'
    assert page_dictionaries['en']['slug'] == 'bulk-item-pickup'
    assert page_dictionaries['en']['short_description'] == 'Twice a year, Austin residential trash and recycling customers can place large items out on the curb to be picked up. These items include appliances, furniture, and carpet.'
    assert page_dictionaries['en']['dynamic_content'] == []
    assert page_dictionaries['en']['steps'] == [
        {'id': '8ae81673-200e-4ef9-a744-28b38752d7ac',
         'type': 'basic_step',
         'value': '<p>Use the this tool to see what bulk items can be picked '
                  'up. Bulk items are items that are too large for your trash '
                  'cart, such as appliances, furniture, and '
                  'carpet.</p><p></p><p><code>APPBLOCK: What do I do '
                  'with</code></p>'},
        {'id': 'c9ad6f3f-5acc-4d19-bbd0-7a9dd6fb847a',
         'type': 'basic_step',
         'value': '<p>Consider donating your items before placing them on the '
                  'curb for pickup.</p>'},
        {'id': 'b69e6dda-c805-4547-b708-e4e09cf679fc',
         'type': 'basic_step',
         'value': '<p>Look up your bulk pickup weeks. We only collect bulk '
                  'items from Austin residential trash and recycling customers '
                  'twice a year, and customers have different pickup '
                  'weeks.</p><p></p><p><code>APPBLOCK: Collection '
                  'Schedule</code></p>'},
        {'id': '1f9762ad-1296-47fd-9623-bb1b8a659f6a',
         'type': 'basic_step',
         'value': '<p>Review the bulk item pickup do’s and don’ts below.</p>'},
        {'id': '2c8e26ed-4ac2-4a0b-a720-3b6c76098973',
         'type': 'basic_step',
         'value': '<p>Place bulk items at the curb in front of your house by '
                  '6:30 am on the first day of your scheduled collection '
                  'week.</p>'},
        {'id': '13fc4079-a860-45cf-96b4-1638caf0f154',
         'type': 'basic_step',
         'value': '<p>Separate items into three '
                  'piles:</p><ul><li>Metal—includes appliances, doors must be '
                  'removed</li><li>Passenger car tires—limit of eight tires per '
                  'household, rims must be removed, no truck or tractor '
                  'tires</li><li>Non-metal items—includes carpeting and '
                  'nail-free lumber</li></ul>'},
        {'id': 'c41f1d29-2822-4ac8-8616-1e8846ec098f',
         'type': 'basic_step',
         'value': '<p>The three separate piles are collected by different '
                  'trucks and may be collected at different times throughout '
                  'the week.</p>'}
    ]
    assert page_dictionaries['en']['topics'] == {'edges': []}
    assert page_dictionaries['en']['additional_content'] == '<h2>Bulk item pickup do’s and don’ts</h2><p>Do not put bulk items in bags, boxes, or other containers. Bags will be treated as extra trash and are subject to extra trash fees.</p><p>Do not place any items under low hanging tree limbs or power lines.</p><p>Do not place items in an alley in any area in front of a vacant lot or in front of a business. Items will not be collected from these areas.</p><p>To prevent damage to your property, keep bulk items 5 feet away from your:</p><ul><li>Trash cart</li><li>Mailbox</li><li>Fences or walls</li><li>Water meter</li><li>Telephone connection box</li><li>Parked cars</li></ul>'
    assert not page_dictionaries['en']['coa_global']


def test_get_dummy_location_page_from_revision(remote_staging_preview_url, remote_pytest_api):
    preview_url = f'{remote_staging_preview_url}/location/UGFnZVJldmlzaW9uTm9kZTozMA==?CMS_API={remote_pytest_api}'

    page_dictionaries = PageImporter(preview_url).fetch_page_data().page_dictionaries
    assert page_dictionaries['en']['title'] == 'Location name [en]'
    assert page_dictionaries['en']['slug'] == 'location-name-en'
    assert not page_dictionaries['en']['coa_global']
    assert page_dictionaries['en']['physical_street'] == '123 Fake St.'
    assert page_dictionaries['en']['physical_unit'] == ''
    assert page_dictionaries['en']['physical_city'] == 'Austin'
    assert page_dictionaries['en']['physical_state'] == 'TX'
    assert page_dictionaries['en']['physical_zip'] == '78745'
    assert page_dictionaries['en']['mailing_street'] == '456 Fake mailing address'
    assert page_dictionaries['en']['mailing_city'] == 'Austin'
    assert page_dictionaries['en']['mailing_state'] == 'TX'
    assert page_dictionaries['en']['mailing_zip'] == '78745'
    assert page_dictionaries['en']['phone_number'] == '+15128675309'
    assert page_dictionaries['en']['phone_description'] == 'Jenny'
    assert page_dictionaries['en']['email'] == 'tommy@tut.one'
    assert page_dictionaries['en']['nearest_bus1'] == 1
    assert page_dictionaries['en']['nearest_bus2'] == 2
    assert page_dictionaries['en']['nearest_bus3'] == 3
    assert page_dictionaries['en']['physical_location_photo'] is None
    assert page_dictionaries['en']['related_services'] == {'edges': [{'node': {
        'related_service': {'title': 'Service page with contact'}, 'hours_same_as_location': False,
        'monday_start_time': '12:00:00', 'monday_end_time': '17:00:00', 'monday_start_time2': None,
        'monday_end_time2': None, 'tuesday_start_time': '12:00:00', 'tuesday_end_time': '17:00:00',
        'tuesday_start_time2': None, 'tuesday_end_time2': None, 'wednesday_start_time': '12:00:00',
        'wednesday_end_time': '17:00:00', 'wednesday_start_time2': None,
        'wednesday_end_time2': None, 'thursday_start_time': '12:00:00',
        'thursday_end_time': '17:00:00', 'thursday_start_time2': None, 'thursday_end_time2': None,
        'friday_start_time': '12:00:00', 'friday_end_time': '17:00:00', 'friday_start_time2': None,
        'friday_end_time2': None, 'saturday_start_time': None, 'saturday_end_time': None,
        'saturday_start_time2': None, 'saturday_end_time2': None, 'sunday_start_time': None,
        'sunday_end_time': None, 'sunday_start_time2': None, 'sunday_end_time2': None,
        'hours_exceptions': ''}}]}
    assert page_dictionaries['en']['monday_start_time'] == '00:00:00'
    assert page_dictionaries['en']['monday_end_time'] == '01:00:00'
    assert page_dictionaries['en']['monday_start_time2'] == '02:00:00'
    assert page_dictionaries['en']['monday_end_time2'] == '03:00:00'
    assert page_dictionaries['en']['tuesday_start_time'] == '04:00:00'
    assert page_dictionaries['en']['tuesday_end_time'] == '05:00:00'
    assert page_dictionaries['en']['tuesday_start_time2'] == '06:00:00'
    assert page_dictionaries['en']['tuesday_end_time2'] == '07:00:00'
    assert page_dictionaries['en']['wednesday_start_time'] == '08:00:00'
    assert page_dictionaries['en']['wednesday_end_time'] == '09:00:00'
    assert page_dictionaries['en']['wednesday_start_time2'] == '10:00:00'
    assert page_dictionaries['en']['wednesday_end_time2'] == '11:00:00'
    assert page_dictionaries['en']['thursday_start_time'] == '12:00:00'
    assert page_dictionaries['en']['thursday_end_time'] == '13:00:00'
    assert page_dictionaries['en']['thursday_start_time2'] == '14:00:00'
    assert page_dictionaries['en']['thursday_end_time2'] == '15:00:00'
    assert page_dictionaries['en']['friday_start_time'] == '16:00:00'
    assert page_dictionaries['en']['friday_end_time'] == '17:00:00'
    assert page_dictionaries['en']['friday_start_time2'] == '18:00:00'
    assert page_dictionaries['en']['friday_end_time2'] == '19:00:00'
    assert page_dictionaries['en']['saturday_start_time'] == '20:00:00'
    assert page_dictionaries['en']['saturday_end_time'] == '21:00:00'
    assert page_dictionaries['en']['saturday_start_time2'] == '22:00:00'
    assert page_dictionaries['en']['saturday_end_time2'] == '23:00:00'
    assert page_dictionaries['en']['sunday_start_time'] is None
    assert page_dictionaries['en']['sunday_end_time'] is None
    assert page_dictionaries['en']['sunday_start_time2'] is None
    assert page_dictionaries['en']['sunday_end_time2'] is None
    assert page_dictionaries['en']['hours_exceptions'] == 'exceptions to hours'

    assert page_dictionaries['en']['slug'] == 'location-name-en'
    assert not page_dictionaries['en']['coa_global']


def test_get_dummy_service_page_with_contact_from_revision(remote_staging_preview_url, remote_pytest_api):
    preview_url = f'{remote_staging_preview_url}/services/UGFnZVJldmlzaW9uTm9kZToyOA==?CMS_API={remote_pytest_api}'

    page_dictionaries = PageImporter(preview_url).fetch_page_data().page_dictionaries
    assert page_dictionaries['en']['title'] == 'Service page with contact'
    assert page_dictionaries['en']['slug'] == 'service-page-with-contact'
    assert page_dictionaries['en']['contacts'] == {'edges': [{'node': {'contact':
        {'name': 'Contact name',
         'phone_number': {'edges': []},
         'email': '',
         'social_media': [],
         'location_page': {'slug': 'location-name-en'}}}}]}
