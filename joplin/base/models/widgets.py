from countable_field import widgets

AUTHOR_LIMITS = {
    "title": 58,
    "description": 254,
    "additional_content": 5000,
    "document_title": 58,
    "authoring_office": 58,
    "summary": 600,
    "mission": 400
}

countConfig = {'data-count': 'characters',
               'data-max-count': 58, 'data-count-direction': 'down'}

countConfigTextArea = {'data-count': 'characters',
                       'data-max-count': 254, 'data-count-direction': 'down'}
countMe = widgets.CountableTextInputWidget(attrs=countConfig)
countMeTextArea = widgets.CountableWidget(attrs=countConfigTextArea)
