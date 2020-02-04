from wagtail.core.models import Page

from users.models import User
from base.models import (
    HomePage,
    InformationPage,
    TopicPage, TopicCollectionPage, TopicPageTopicCollection,
    DepartmentPage
)

def load_test_data():
    home = HomePage.objects.first()

    # Create test user
    user = User.objects.create_superuser(
        "test@austintexas.io",
        "test_password",
        is_staff=True,
        is_active=True,
        is_superuser=True,
    )

    # Create Test Topic Collection Page
    topic_collection = TopicCollectionPage(**{
        'title': "Pets",
        'owner': user,
    })
    home.add_child(instance=topic_collection)
    topic_collection.save_revision()

    # Create Test Topic Page
    topic = TopicPage(**{
        'title': "Pet Adoption",
        'owner': user,
    })
    topic_page_topic_collection = TopicPageTopicCollection(**{
        "page": topic,
        "topiccollection": topic_collection,
    })
    topic.topiccollections.add(topic_page_topic_collection)
    home.add_child(instance=topic)
    topic.save_revision()

    # Create Test DepartmentPage
    department = DepartmentPage(**{
        'title': "Department of Animals",
        'owner': user,
    })
    home.add_child(instance=department)
    department.save_revision()

    # Create Test Topic Page
    info_page = InformationPage(**{
        'title': "Adopt a baby tarantula",
        'owner': user,
    })
    home.add_child(instance=info_page)
    info_page.save_revision()
    # Pages default to "Live" when first created
    # Only unpublish "info_page"
    # We want the topic, topic_collection, and department to be "Live"
    info_page.unpublish()

    return {
        "user": user,
        "info_page": info_page,
        "topic": topic,
        "topic_collection": topic_collection,
        "department": department,
    }
