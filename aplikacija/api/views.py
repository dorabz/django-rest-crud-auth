from rest_framework import generics
from api import serializers
from django.contrib.auth.models import User
from api.models import Recipe
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly,IsUserOrReadOnly
from rest_framework import status, viewsets, mixins
from rest_framework.exceptions import NotFound

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsUserOrReadOnly]
   
class CreateUserView(generics.CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = serializers.UserSerializer

class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

class UserRecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().select_related(
        'owner'
        )
    serializer_class = serializers.RecipeSerializer
    
    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs.get("user_pk")
        try:
            owner = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound('A user with this id does not exist')
        return self.queryset.filter(owner=owner)
