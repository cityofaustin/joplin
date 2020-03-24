import pytest
from importer.page_importer import PageImporter
# from unittest.mock import patch


def test_parse_janis_preview_url():
    preview_url = 'https://janis.austintexas.io/en/preview/information/UGFnZVJldmlzaW9uTm9kZToyNjI4'

    page_importer = PageImporter(preview_url)

    assert page_importer.joplin_api_endpoint == 'https://joplin-staging.herokuapp.com/api/graphql'
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'information'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToyNjI4'


def test_parse_topic_page_dummy_data_janis_preview_url():
    preview_url = 'http://janis-austin-gov-staging.s3-website-us-east-1.amazonaws.com/en/preview/topic/UGFnZVJldmlzaW9uTm9kZToxMg==?CMS_API=https://joplin-pr-4116-importer-j2-tes.herokuapp.com/api/graphql'

    page_importer = PageImporter(preview_url)

    assert page_importer.joplin_api_endpoint == 'https://joplin-pr-4116-importer-j2-tes.herokuapp.com/api/graphql'
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'topic'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToxMg=='


def test_parse_topic_collection_page_dummy_data_janis_preview_url():
    preview_url = 'http://janis-austin-gov-staging.s3-website-us-east-1.amazonaws.com/en/preview/topiccollection/UGFnZVJldmlzaW9uTm9kZToxMw==?CMS_API=https://joplin-pr-4116-importer-j2-tes.herokuapp.com/api/graphql'

    page_importer = PageImporter(preview_url)

    assert page_importer.joplin_api_endpoint == 'https://joplin-pr-4116-importer-j2-tes.herokuapp.com/api/graphql'
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'topiccollection'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToxMw=='


def test_parse_information_page_dummy_data_janis_preview_url():
    preview_url = 'http://janis-austin-gov-staging.s3-website-us-east-1.amazonaws.com/en/preview/information/UGFnZVJldmlzaW9uTm9kZToxMQ==?CMS_API=https://joplin-pr-4116-importer-j2-tes.herokuapp.com/api/graphql'

    page_importer = PageImporter(preview_url)

    assert page_importer.joplin_api_endpoint == 'https://joplin-pr-4116-importer-j2-tes.herokuapp.com/api/graphql'
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'information'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZToxMQ=='


def test_parse_service_page_dummy_data_janis_preview_url():
    preview_url = 'https://janis.austintexas.io/en/preview/services/UGFnZVJldmlzaW9uTm9kZTozNDQ4'

    page_importer = PageImporter(preview_url)

    assert page_importer.joplin_api_endpoint == 'https://joplin-staging.herokuapp.com/api/graphql'
    assert page_importer.language == 'en'
    assert page_importer.page_type == 'services'
    assert page_importer.revision_id == 'UGFnZVJldmlzaW9uTm9kZTozNDQ4'


# this test will start breaking once we no longer have this revision in the db
# todo: figure out a good way to mock api responses
def test_get_information_page_from_revision():
    preview_url = 'https://janis.austintexas.io/en/preview/information/UGFnZVJldmlzaW9uTm9kZToyNjI4'

    page_dictionary = PageImporter(preview_url).fetch_page_data().page_dictionary

    assert page_dictionary['id'] == 'SW5mb3JtYXRpb25QYWdlTm9kZToxMjM='
    assert page_dictionary['title'] == 'Fire safety checklist for mobile food vendors'
    assert page_dictionary['description'] == 'Any mobile food vendor who uses propane or propane accessories and operates in the City of Austin or Travis County must get a fire safety inspection.'


# this test will start breaking once we no longer have this revision in the db
# todo: figure out a good way to mock api responses
# https://docs.python.org/3/library/unittest.mock.html
# @patch('module.ClassName2')
def test_get_dummy_topic_collection_page_from_revision():
    preview_url = 'http://janis-austin-gov-staging.s3-website-us-east-1.amazonaws.com/en/preview/topiccollection/UGFnZVJldmlzaW9uTm9kZToxMw==?CMS_API=https://joplin-pr-4116-importer-j2-tes.herokuapp.com/api/graphql'

    page_dictionary = PageImporter(preview_url).fetch_page_data().page_dictionary

    assert page_dictionary['id'] == 'VG9waWNDb2xsZWN0aW9uTm9kZTo0'
    assert page_dictionary['title'] == 'topic collection title [en]'
    assert page_dictionary['slug'] == 'topic-collection-title-en'
    assert page_dictionary['description'] == 'topic collection description [en]'

    # adding themes as a part of our topic collection query
    # instead of importing/testing them separately
    assert page_dictionary['theme'] == {
        'id': 'VGhlbWVOb2RlOjE=',
        'slug': 'theme-slug-en',
        'text': 'theme text [en]',
        'description': 'theme description [en]'
    }

# this test will start breaking once we no longer have this revision in the db
# todo: figure out a good way to mock api responses
# https://docs.python.org/3/library/unittest.mock.html
# @patch('module.ClassName2')
def test_get_dummy_topic_page_from_revision():
    preview_url = 'http://janis-austin-gov-staging.s3-website-us-east-1.amazonaws.com/en/preview/topic/UGFnZVJldmlzaW9uTm9kZToxMg==?CMS_API=https://joplin-pr-4116-importer-j2-tes.herokuapp.com/api/graphql'

    page_dictionary = PageImporter(preview_url).fetch_page_data().page_dictionary

    assert page_dictionary['id'] == 'VG9waWNOb2RlOjU='
    assert page_dictionary['title'] == 'topic title [en]'
    assert page_dictionary['slug'] == 'topic-title-en'
    assert page_dictionary['description'] == 'topic description [en]'
    assert page_dictionary['topiccollections'] == {
        'edges': [{
            'node': {
                'topiccollection': {
                    'id': 'VG9waWNDb2xsZWN0aW9uTm9kZTo0',
                    'title': 'topic collection title [en]',
                    'slug': 'topic-collection-title-en',
                    'description': 'topic collection description [en]',
                    'theme': {
                        'id': 'VGhlbWVOb2RlOjE=',
                        'slug': 'theme-slug-en',
                        'text': 'theme text [en]',
                        'description': 'theme description [en]'
                    },
                    'liveRevision': {
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
def test_get_dummy_information_page_from_revision():
    preview_url = 'http://janis-austin-gov-staging.s3-website-us-east-1.amazonaws.com/en/preview/information/UGFnZVJldmlzaW9uTm9kZToxMQ==?CMS_API=https://joplin-pr-4116-importer-j2-tes.herokuapp.com/api/graphql'

    page_dictionary = PageImporter(preview_url).fetch_page_data().page_dictionary

    assert page_dictionary['id'] == 'SW5mb3JtYXRpb25QYWdlTm9kZTo2'
    assert page_dictionary['title'] == 'information page title [en]'
    assert page_dictionary['slug'] == 'information-page-title-en'
    assert page_dictionary['description'] == 'information page description [en]'
    assert page_dictionary['topics'] == {
        'edges': [{
            'node': {
                'topic': {
                    'id': 'VG9waWNOb2RlOjU=',
                    'title': 'topic title [en]',
                    'slug': 'topic-title-en',
                    'description': 'topic description [en]',
                    'topiccollections': {
                        'edges': [{
                            'node': {
                                'topiccollection': {
                                    'id': 'VG9waWNDb2xsZWN0aW9uTm9kZTo0',
                                    'title': 'topic collection title [en]',
                                    'slug': 'topic-collection-title-en',
                                    'description': 'topic collection description [en]',
                                    'theme': {
                                        'id': 'VGhlbWVOb2RlOjE=',
                                        'slug': 'theme-slug-en',
                                        'text': 'theme text [en]',
                                        'description': 'theme description [en]'
                                    },
                                    'liveRevision': {
                                        'id': 'UGFnZVJldmlzaW9uTm9kZToz'
                                    }
                                }
                            }
                        }]
                    },
                    'liveRevision': {
                        'id': 'UGFnZVJldmlzaW9uTm9kZToxMg=='
                    }
                }
            }
        }]
    }
    assert page_dictionary['additionalContent'] == '<p>information page additional content [en]</p>'
    #     todo contacts
    assert not page_dictionary['coaGlobal']


def test_get_dummy_service_page_from_revision():
    preview_url = 'https://janis.austintexas.io/en/preview/services/UGFnZVJldmlzaW9uTm9kZTozNDQ4'

    page_dictionary = PageImporter(preview_url).fetch_page_data().page_dictionary
    assert page_dictionary['id'] == 'U2VydmljZVBhZ2VOb2RlOjU='
    assert page_dictionary['title'] == 'Get your bulk items collectedd'
    assert page_dictionary['slug'] == 'bulk-item-pickup'
    assert page_dictionary['shortDescription'] == 'Twice a year, Austin residential trash and recycling customers can place large items out on the curb to be picked up. These items include appliances, furniture, and carpet.'
    assert page_dictionary['dynamicContent'] == []
    assert page_dictionary['steps'] == [
        {   'id': '387583c9-5aaa-40b2-acdb-a197e32a4f6d',
            'type': 'basic_step',
            'value': '<p>Use the this tool to see what bulk items can be picked '
                     'up. Bulk items are items that are too large for your trash '
                     'cart, such as appliances, furniture, and '
                     'carpet.</p><p></p><p><code>APPBLOCK: What do I do '
                     'with</code></p>'},
        {   'id': '3b80d7f5-1cce-480f-be13-217784eabcd9',
            'type': 'basic_step',
            'value': '<p>Consider donating your items before placing them on the '
                     'curb for pickup.</p>'},
        {   'id': '15b9a848-91ed-41be-857a-0b44a5580eb0',
            'type': 'basic_step',
            'value': '<p>Look up your bulk pickup weeks. We only collect bulk '
                     'items from Austin residential trash and recycling customers '
                     'twice a year, and customers have different pickup '
                     'weeks.</p><p></p><p><code>APPBLOCK: Collection '
                     'Schedule</code></p>'},
        {   'id': 'a8b677b9-d8d0-4c45-baa6-894e4e504c97',
            'type': 'basic_step',
            'value': '<p>Review the bulk item pickup do’s and don’ts below.</p>'},
        {   'id': '9cce1999-8a7f-4400-922d-ae6b03e41d68',
            'type': 'basic_step',
            'value': '<p>Place bulk items at the curb in front of your house by '
                     '6:30 am on the first day of your scheduled collection '
                     'week.</p>'},
        {   'id': 'bb6b732d-177d-4a89-b179-882f2166aa63',
            'type': 'basic_step',
            'value': '<p>Separate items into three '
                     'piles:</p><ul><li>Metal—includes appliances, doors must be '
                     'removed</li><li>Passenger car tires—limit of eight tires per '
                     'household, rims must be removed, no truck or tractor '
                     'tires</li><li>Non-metal items—includes carpeting and '
                     'nail-free lumber</li></ul>'},
        {   'id': '47a7c5da-7afe-4fd0-9de0-03045938ef24',
            'type': 'basic_step',
            'value': '<p>The three separate piles are collected by different '
                     'trucks and may be collected at different times throughout '
                     'the week.</p>'}
    ]
    assert page_dictionary['topics'] == { 'edges': [] }
    assert page_dictionary['additionalContent'] == '<h2>Bulk item pickup do’s and don’ts</h2><p>Do not put bulk items in bags, boxes, or other containers. Bags will be treated as extra trash and are subject to extra trash fees.</p><p>Do not place any items under low hanging tree limbs or power lines.</p><p>Do not place items in an alley in any area in front of a vacant lot or in front of a business. Items will not be collected from these areas.</p><p>To prevent damage to your property, keep bulk items 5 feet away from your:</p><ul><li>Trash cart</li><li>Mailbox</li><li>Fences or walls</li><li>Water meter</li><li>Telephone connection box</li><li>Parked cars</li></ul>'
    assert not page_dictionary['coaGlobal']
