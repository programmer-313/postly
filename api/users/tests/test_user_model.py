from django.test import TestCase

from users.models import User


class TestUserModel(TestCase):

    # setting up the model instances
    def setUp(self) -> None:
        self.test_pass = "django_test_client"
        self.n = 3
        for i in range(self.n):
            User.objects.create(email=f"testuser{i+1}@example.com", password=self.test_pass)
        print("")

    # testing retrieve operation
    def test_get_users(self):
        assert User.objects.all().count() == self.n

    def test_get_user_with_email(self):
        for i in range(self.n):
            user = User.objects.get(email=f"testuser{i+1}@example.com")
            assert user.email == f"testuser{i+1}@example.com"
            assert user.is_verified == False
            assert user.is_active == False

    # testing update operation
    def test_update_user_instances(self):
        for i in range(self.n):
            user = User.objects.get(email=f"testuser{i+1}@example.com")
            user.first_name = f"Test{i+1}"
            user.last_name = "User"
            user.save()
            assert user.first_name == f"Test{i+1}"
            assert user.last_name == "User"

    # test delete operations
    def test_delete_user_instance(self):
        initial_users = User.objects.all().count()
        assert initial_users == self.n
        print(User.objects.all())
        user = User.objects.get(email="testuser3@example.com")
        user.delete()
        assert User.objects.all().count() == (self.n - 1)
