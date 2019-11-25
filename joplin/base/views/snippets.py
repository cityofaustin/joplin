from urllib.parse import urlencode

from django.apps import apps
from django.contrib.admin.utils import quote, unquote
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import capfirst
from django.utils.translation import ugettext as _

from wagtail.admin import messages
from wagtail.admin.edit_handlers import ObjectList, extract_panel_definitions_from_model_class
from wagtail.admin.utils import permission_denied
from wagtail.snippets.models import get_snippet_models
from wagtail.snippets.permissions import get_permission_name, user_can_edit_snippet_type


# == Helper functions ==
def get_snippet_model_from_url_params(app_name, model_name):
    """
    Retrieve a model from an app_label / model_name combo.
    Raise Http404 if the model is not a valid snippet type.
    """
    print('snippets.py', app_name, model_name)
    try:
        model = apps.get_model(app_name, model_name)
    except LookupError:
        raise Http404
    if model not in get_snippet_models():
        # don't allow people to hack the URL to edit content types that aren't registered as snippets
        raise Http404

    return model


SNIPPET_EDIT_HANDLERS = {}


def get_snippet_edit_handler(model):
    if model not in SNIPPET_EDIT_HANDLERS:
        if hasattr(model, 'edit_handler'):
            # use the edit handler specified on the page class
            edit_handler = model.edit_handler
        else:
            panels = extract_panel_definitions_from_model_class(model)
            edit_handler = ObjectList(panels)

        SNIPPET_EDIT_HANDLERS[model] = edit_handler.bind_to(model=model)

    return SNIPPET_EDIT_HANDLERS[model]


# == Views ==


def edit(request, app_label, model_name, pk):
    print('YESSS THIS WORKED')
    model = get_snippet_model_from_url_params(app_label, model_name)

    permission = get_permission_name('change', model)
    if not request.user.has_perm(permission):
        return permission_denied(request)

    instance = get_object_or_404(model, pk=unquote(pk))
    edit_handler = get_snippet_edit_handler(model)
    edit_handler = edit_handler.bind_to(instance=instance, request=request)
    form_class = edit_handler.get_form_class()

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                _("{snippet_type} '{instance}' updated.").format(
                    snippet_type=capfirst(model._meta.verbose_name_plural),
                    instance=instance
                ),
                buttons=[
                    messages.button(reverse(
                        'wagtailsnippets:edit', args=(app_label, model_name, quote(instance.pk))
                    ), _('Edit'))
                ]
            )
            return redirect('wagtailsnippets:list', app_label, model_name)
        else:
            messages.validation_error(
                request, _("The snippet could not be saved due to errors."), form
            )
    else:
        form = form_class(instance=instance)

    edit_handler = edit_handler.bind_to(form=form)

    return render(request, 'wagtailsnippets/snippets/edit.html', {
        'can_delete_snippets': request.user.has_perm(get_permission_name('delete', model)),
        'model_opts': model._meta,
        'instance': instance,
        'edit_handler': edit_handler,
        'form': form,
    })
