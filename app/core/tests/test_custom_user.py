from decimal import Decimal

from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase

def create_user(email='test@test.com', password='test123'):
    return get_user_model().objects.create_user(email, password)
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

    def test_create_recipe(self):
        user = get_user_model().objects.create_user('test@example.com', 'testpass23')
        recipe = models.Recipe.objects.create(
            user=user,
            title='Test Recipe',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe'
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='tag1')
        self.assertEqual(str(tag), tag.name)