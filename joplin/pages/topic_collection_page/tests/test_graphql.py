import pytest
from django.utils import translation

from pages.topic_page.fixtures import kitchen_sink as create_topic
from pages.service_page.fixtures import kitchen_sink as create_top_page
from pages.topic_page.factories import TopicPageTopPageFactory


# Make sure that we return English slugs for top pages, even for Spanish pages
@pytest.mark.django_db
def test_spanish_slugs_for_top_pages(run_graphql):
    top_page = create_top_page()
    top_page.slug_en = "english-slug"
    top_page.slug_es = "spanish-slug"
    top_page.title_en = "english_title"
    top_page.title_es = "spanish_title"
    top_page.save()
    topic = create_topic()
    # Adds a top page to a topic page
    TopicPageTopPageFactory(topic=topic, page=top_page)
    topic_collection_query = """
      query getTopicCollectionTopics($id: ID) {
        topicCollectionTopics(topicCollection: $id) {
          edges {
            node {
              page {
                topicpage {
                  id
                  live
                  slug
                  title
                  description
                  topPages {
                    edges {
                      node {
                        title
                        slug
                        pageType
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    """

    def get_top_page(graphql_result):
        return graphql_result['topicCollectionTopics']['edges'][0]['node']['page']['topicpage']['topPages']['edges'][0]['node']

    # Hack to make django return Spanish values.
    # Same effect as setting Accept-Language:ES header.
    translation.activate('es')
    spanish_result = run_graphql(topic_collection_query)
    assert get_top_page(spanish_result)['title'] == "spanish_title"
    assert get_top_page(spanish_result)['slug'] == "english-slug"

    translation.activate('en')
    english_result = run_graphql(topic_collection_query)
    assert get_top_page(english_result)['title'] == "english_title"
    assert get_top_page(english_result)['slug'] == "english-slug"
