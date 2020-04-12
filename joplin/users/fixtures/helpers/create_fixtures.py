from users.models import User
from users.factories import UserFactory


# Skips creating fixture if User with email already exists
def create_fixture(user_data, fixture_name):
    try:
        user = User.objects.get(slug=user_data['email'])
    except User.DoesNotExist:
        user = None
    if user:
        print(f"Skipping user fixture: {fixture_name}")
        return user

    user = UserFactory.create(**user_data)
    print(f"Built user fixture: {fixture_name}")
    return user
