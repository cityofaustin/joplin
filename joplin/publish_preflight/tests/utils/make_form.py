from django.contrib.contenttypes.models import ContentType


# Logic extracted from wagtail/admin/views/pages.py
def make_form(page, fake_request):
    parent = page.get_parent()
    content_type = ContentType.objects.get_for_model(page)
    page_class = content_type.model_class()

    edit_handler = page_class.get_edit_handler()
    edit_handler = edit_handler.bind_to(instance=page, request=fake_request)
    # We must use the edit handler's form_class rather than page.specific.base_form_class
    # Because the edit_handler adds critical _meta information required to construct a form
    form_class = edit_handler.get_form_class()

    form = form_class(fake_request, instance=page, parent_page=parent)
    return form
