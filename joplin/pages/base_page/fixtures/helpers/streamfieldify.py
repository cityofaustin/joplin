import json

# Turns a dictionary into Streamfield-parseable raw json object
def streamfieldify(data):
    return json.dumps(to_unicode(data))


# Converts all strings to unicode
def to_unicode(data):
    if type(data) is dict:
        return dict([
            (to_unicode(k), to_unicode(v))
            for k,v in data.items()
        ])
    elif type(data) is list:
        return [
            to_unicode(v)
            for v in data
        ]
    elif type(data) is str:
        return u'{0}'.format(data)
    else:
        return data
