def make_form_from_fake_request(page, fake_request):
    parent = page.get_parent()
    form_class = page.specific.base_form_class
    form = form_class(fake_request, instance=page, parent_page=parent)
    return form
