from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Recipe
 
#  serializer - converting complex data such as querysets and model instances to be converted into data
#  types understandable by javascript and front-end frameworks e.g JSON 


class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'owner']

class UserSerializer(serializers.ModelSerializer):
    recipes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'recipes']
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
        username=validated_data['username'],
        first_name=validated_data['first_name'],
    )
        user.set_password(validated_data['password'])
        user.save()
        return user
