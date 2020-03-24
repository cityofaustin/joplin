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