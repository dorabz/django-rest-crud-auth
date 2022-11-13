import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.serializers import UserSerializer, RecipeSerializer
from api.views import UserDetail
from api.models import Recipe

from django.contrib import auth
from rest_framework.test import APIClient

class CreateUserTestCase(APITestCase):

    # User - Create (Token auth - for API) 😊
    def test_registration(self):
        data = {"username": "branko", "first_name": "Branko", "password": "brankobranko"}
        response = self.client.post("/api/users/new/", data)
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = Token.objects.get(user__username='branko')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key) # token will be included in all requests - login alias

     # User - Login (Session based - for web browser) 😊
    def test_login(self):
        data = {"username": "leon", "password": "leonleon"}
        response = self.client.post("/api-auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserListTestCase(APITestCase):

    # Users - Read List (Doesn't need auth for READ) 😊
    def test_userList(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RecipeListTestCase(APITestCase):

    # Recipes - Read List (Doesn't need auth for READ) 😊
    def test_recipesList(self):
        response = self.client.get("/api/recipes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserDetailTestCase(APITestCase):

    #  Recipe - CREATE 😊
    def test_RecipeCRUD(self):

        # User - Create & Login - Auth needed to create,update,delete recipe (Token auth - for API) 😊
        data = {"username": "branko", "first_name": "Branko", "password": "brankobranko"}
        response = self.client.post("/api/users/new/", data)
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = Token.objects.get(user__username='branko')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key) # token will be included in all requests - login alias
        
        # recipe create in browser mode
        recipe_det = Recipe.objects.create(name = "špagete", description = "ukusne špagete", owner = user)
        response = client.get(reverse("recipe-detail", kwargs={'pk': recipe_det.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Recipe - CREATE - (Token auth - for API) 😊
        response = client.post("/api/recipes/", {'name': 'lazanje', 'description': 'ukusne lazanje'}, format="json")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        test_against = Recipe.objects.get(name='lazanje')

        # Recipe - READ DETAIL - doesn't need auth, here for check Recipe - CREATE 😊
        response = client.get(reverse("recipe-detail", kwargs={'pk': test_against.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #  Nested - READ recipes of user - 😊
        response = self.client.get(reverse("user-recipe", kwargs={'user_pk': user.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Recipe - UPDATE - (Token auth - for API) 😊
        response = client.patch(reverse("recipe-detail", kwargs={'pk': test_against.id}), {'name': 'lazanje s mesom'}, format="json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        test_against = Recipe.objects.get(id = test_against.id)
        self.assertAlmostEqual(test_against.name, "lazanje s mesom")

        # Recipe - DELETE - (Token auth - for API) 😊
        response = client.delete(reverse("recipe-detail", kwargs={'pk': test_against.id}), format="json")
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # Recipe - READ DETAIL - doesn't need auth, here for check Recipe - DELETE 😊
        response = client.get(reverse("recipe-detail", kwargs={'pk': test_against.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # not found because we deleted object


        # User - READ DETAIL - doesn't need auth, here for check  😊         
        response = self.client.get(reverse("user-detail", kwargs={'pk': user.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User - UPDATE - (Token auth - for API) 😊    
        response = client.patch(reverse("user-detail", kwargs={'pk': user.id}), {'first_name': 'BRANIMIR'}, format="json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        test_against_user = User.objects.get(id = user.id)
        self.assertAlmostEqual(test_against_user.first_name, "BRANIMIR")
 
        # User - DELETE - (Token auth - for API) 😊
        response = client.delete(reverse("user-detail", kwargs={'pk': user.id}), format="json")
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # User - READ DETAIL - doesn't need auth, here for check Recipe - DELETE 😊
        response = client.get(reverse("user-detail", kwargs={'pk': user.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # unauthorized because you deleted your account and automatically logged out

