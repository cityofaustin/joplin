import factory
from users.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        # Use our custom UserManager to create_user
        manager = cls._get_manager(target_class)
        email = kwargs.pop("email")
        password = kwargs.pop("password", None)
        return manager.create_user(email, password, **kwargs)
