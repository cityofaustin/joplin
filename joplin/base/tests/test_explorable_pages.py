import pytest

def test_explorable_pages(self):
    event_editor = get_user_model().objects.get(username='eventeditor')
    christmas_page = EventPage.objects.get(url_path='/home/events/christmas/')
    unpublished_event_page = EventPage.objects.get(url_path='/home/events/tentative-unpublished-event/')
    someone_elses_event_page = EventPage.objects.get(url_path='/home/events/someone-elses-event/')
    about_us_page = Page.objects.get(url_path='/home/about-us/')

    user_perms = UserPagePermissionsProxy(event_editor)
    explorable_pages = user_perms.explorable_pages()

    # Verify all pages below /home/events/ are explorable
    self.assertTrue(explorable_pages.filter(id=christmas_page.id).exists())
    self.assertTrue(explorable_pages.filter(id=unpublished_event_page.id).exists())
    self.assertTrue(explorable_pages.filter(id=someone_elses_event_page.id).exists())

    # Verify page outside /events/ tree are not explorable
    self.assertFalse(explorable_pages.filter(id=about_us_page.id).exists())
