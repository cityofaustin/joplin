import factory
from users.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
