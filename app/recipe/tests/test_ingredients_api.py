from core.models import Ingredient
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import IngredientSerializer
from rest_framework import status
from rest_framework.test import APIClient


INGREDIENT_URL = reverse('recipe:ingredient-list')


def detail_url(ing_id):
    return reverse('recipe:ingredient-detail', args=[ing_id])

def create_user(email='user@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email, password)

class PublicIngredientAPI(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientAPI(TestCase):

    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Vanilla')
        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        user2 = create_user(email='user2@example.com')
        ing = Ingredient.objects.create(user=self.user, name='Salt')
        Ingredient.objects.create(user=user2, name='Pepper')
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ing.name)
        self.assertEqual(res.data[0]['id'], ing.id)


    def test_update_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user, name='Fruit')
        payload = {'name': 'Vegan'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user, name='Fruit')
        url = detail_url(ingredient.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredient.objects.filter(id=ingredient.id).exists())

