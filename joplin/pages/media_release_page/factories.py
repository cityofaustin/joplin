from pages.media_release_page.models import MediaReleasePage
from pages.topic_page.factories import JanisBasePageFactory


class MediaReleasePageFactory(JanisBasePageFactory):
    class Meta:
        model = MediaReleasePage
