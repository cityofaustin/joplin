"""
from publish_preflight.forms import PublishPreflightForm


keeping this for refrence, if there is custom validation we need to do for a page,
we can extend it like so:

class MySuperCoolNewForm(PublishPreflightForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # super cool stuff here

Then, in that model, set base_form_class = MySuperCoolNewForm

More on this here:
https://docs.wagtail.io/en/v2.7/advanced_topics/customisation/page_editing_interface.html#customising-generated-forms

PublishPreflightForm is intended for stuff where we want behavior to be allowed for saving drafts, but not for publishing
So, we might want additional validation here if we need to do other stuff like:
 * automatically add fields
 * geocode address imput
 * clean or modify user input on submit
 * other things I can't think of atm 
"""
