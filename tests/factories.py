from factory.django import DjangoModelFactory
from faker import Factory
from users.models import User

faker = Factory.create()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = faker.name()
    email = faker.email()
    bio = "example bio"
