from users.models import User
from users.factories import UserFactory


# Skips creating fixture if User with email already exists
def create_fixture(user_data, fixture_name, group_list=[]):
    try:
        user = User.objects.get(email=user_data['email'])
    except User.DoesNotExist:
        user = None
    if user:
        print(f"Skipping user fixture: {fixture_name}")
        return user

    user = UserFactory.create(**user_data)
    if len(group_list) > 0:
        user.groups.set(group_list)
    print(f"Built user fixture: {fixture_name}")
    return user
