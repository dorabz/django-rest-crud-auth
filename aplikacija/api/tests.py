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

class CreateUserTestCase(APITestCase):

    # User - Create 😊
    def test_registration(self):
        data = {"username": "branko", "email": "branko@hr.com", "first_name": "Branko", "password": "brankobranko"}
        response = self.client.post("/api/users/new/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

     # User - Login 😊
    def test_login(self):
        data = {"username": "leon", "password": "leonleon"}
        response = self.client.post("/api-auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserListTestCase(APITestCase):

    # Users- Read List 😊
    def test_userList(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RecipeListTestCase(APITestCase):

    # Recipes - Read List 😊
    def test_recipesList(self):
        response = self.client.get("/api/recipes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateUserTestCase(APITestCase):

    # what needs to be done before test function is run 😊
    def setUp(self):
        data = {"username": "branko", "email": "branko@hr.com", "first_name": "Branko", "password": "brankobranko"}
        self.client.post("/api/users/new/", data)
        data = {"username": "Branko", "password": "brankobranko"}
        self.client.post("/api-auth/login/", data)


     #  Recipe - Create 😊
    def test_recipeCreate(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        recipe_det = Recipe.objects.create(name = "špagete", description = "ukusne špagete", owner = user)
        response = self.client.get(reverse("recipe-detail", kwargs={'pk': recipe_det.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class DetailTestCase(APITestCase):

    def setUp(self):
        data = {"username": "branko", "email": "branko@hr.com", "first_name": "Branko", "password": "brankobranko"}
        self.client.post("/api/users/new/", data)
        data = {"username": "Branko", "password": "brankobranko"}
        self.client.post("/api-auth/login/", data)
  
    # User - Read detail 😊
    def test_userDetail(self):
        user_det = User.objects.get()
        response = self.client.get(reverse("user-detail", kwargs={'pk': user_det.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # User - Update
    def test_userUpdate(self):
        user_det = User.objects.get()
        data_change = {"first_name": "Brankec"}
        response = self.client.put(reverse("user-detail", kwargs={'pk': user_det.id}), data_change, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # User - Delete
    def test_userDelete(self):
        user_det = User.objects.get()
        response = self.client.delete(reverse("user-detail", kwargs={'pk': user_det.id}), format="json", follow= True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

     # Recipe - Read detail 😊
    def test_recipeDetail(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        recipe_det = Recipe.objects.create(name = "špagete", description = "ukusne špagete", owner = user)
        response = self.client.get(reverse("recipe-detail", kwargs={'pk': recipe_det.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #  Recipe - Update 😊 - treba popraviti
    def test_recipeUpdate(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        recipe_det = Recipe.objects.create(name = "špagete", description = "ukusne špagete", owner = user)
        recipe_det_up = Recipe.objects.update(name = "špagete1", description = "ukusne špagete", owner = user)
        self.assertEqual(recipe_det_up, 1) # uspješan update
        recipe_obj = Recipe.objects.get(id = 1)
        self.assertEqual(recipe_obj.name, "špagete1")
        response = self.client.get(reverse("recipe-detail", kwargs={'pk': recipe_det.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #  Recipe - Delete 
    def test_recipeDelete(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        recipe_det = Recipe.objects.create(name = "špagete", description = "ukusne špagete", owner = user)
        recipe_det.delete
        response = self.client.delete(reverse("recipe-detail", kwargs={'pk': recipe_det.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #  Nested - Read - 😊
    def test_recipesOfUserList(self):
        user_det = User.objects.get()
        response = self.client.get(reverse("user-recipe", kwargs={'user_pk': user_det.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)