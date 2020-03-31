from urllib.parse import urlencode
from django.http import QueryDict
from users.forms import CustomUserCreationForm


'''
    Logic within make_user_form() is extracted from joplin/users/views/users.py

    user_data is a mock of request.POST data from Joplin.
    user_data must follow the exact structure that request.POST uses in order for tests to be valid.
    To get an accurate example of user_data:
        1. Set a breakpoint in pycharm in the create() function of joplin/users/views/users.py, where you can access request.POST.
        2. Submit a new user from the Joplin UI.
        3. Make a copy of the request.POST data to make your new user_data test case.
'''
def make_user_form(user_data):
    query_dict = QueryDict(urlencode(user_data))
    return CustomUserCreationForm(query_dict)
