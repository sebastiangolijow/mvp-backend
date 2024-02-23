from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTest(TestCase):

    def test_create_user(self):
        email = 'test@test.com'
        password = 'mySuperSecretPassword'
        user = get_user_model().objects.create_user(email=email, password=password, username='test')
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalizer(self):
        sample_emails = [['test1@EXAMPLE.com', 'test1@example.com'], ['Test2@Example.com', 'Test2@example.com'], ['TEST3@EXAMPLE.COM', 'TEST3@example.com']]
        for email, expected in sample_emails:
            user= get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_raise_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email='superuser@email.com', password='test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)