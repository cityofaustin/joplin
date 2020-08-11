import os
from django.http import HttpResponse
from django.conf import settings
from wagtail.admin import messages
from wagtail.core import hooks
from smtplib import SMTPException
from wagtail.admin.forms.auth import PasswordResetForm


@hooks.register('after_create_user')
def send_new_user_email(request, user):
    '''
        Sends an email to a user created by the wagtail users view.
        The PasswordResetForm sends an email when its saved, so we're utilizing that same flow here.

        new_user_form.save() parameters are modified from django.contrib.auth.views.PasswordResetView
        When the new_user_form is saved, the "welcome" email is sent. See: django.contrib.auth.forms.PasswordResetForm
        This function does not create a new user, it just sends the welcome email.
    '''
    new_user_form = PasswordResetForm({"email": user.email})
    try:
        if new_user_form.is_valid():  # is_valid() creates required cleaned_data attribute
            new_user_form.save(**{
                "use_https": True,
                "email_template_name": "joplin_UI/email/new_user.txt",
                "html_email_template_name": "joplin_UI/email/new_user.html",
                "subject_template_name": "joplin_UI/email/new_user_subject.txt",
                "domain_override": settings.BASE_URL,
                "extra_email_context": {
                    "styleguide_url": os.getenv('STYLEGUIDE_URL', ""),
                }
            })
    except SMTPException as e:
        messages.error(request, f"Failed to send email to {user.email}.")
