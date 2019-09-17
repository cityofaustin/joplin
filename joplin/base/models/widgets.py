from countable_field import widgets

"""
copied from
https://docs.google.com/spreadsheets/d/1ZkH93F4tJ0_Zjx4t8k6k6TgwSlOh8u8ejWmegE6WqH0/edit#gid=46035360
TODO: come up with better names/structure to make these settings easy to refer to
( the current names are based on the content model in google sheets)
Should these be in constants or here where it's most relevant?

These limits are NOT to be confused with character limits we might set in the database
(Those limits may be greater)
This allows for spillover/going negative on the character count and also helps keep tables consistent
These limits are more about content than about data schema or performance
"""


GENERIC_TITLE_LIMIT = 58
GENERIC_DESCRIPTION_LIMIT = 254

AUTHOR_LIMITS = {

    "title": GENERIC_TITLE_LIMIT,
    "description": 254,
    "additional_content": 5000,
    "document_title": GENERIC_TITLE_LIMIT,
    "authoring_office": GENERIC_TITLE_LIMIT,
    "document_summary": 600,
    "document_name": GENERIC_TITLE_LIMIT,
    "mission": 400,
    "about_director": 600,

}

countConfig = {'data-count': 'characters',
               'data-max-count': 58, 'data-count-direction': 'down'}

countConfigTextArea = {'data-count': 'characters',
                       'data-max-count': 254, 'data-count-direction': 'down'}
countMe = widgets.CountableTextInputWidget(attrs=countConfig)
countMeTextArea = widgets.CountableWidget(attrs=countConfigTextArea)
