# Kreirano
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('users/new/', views.CreateUserView.as_view()),
    path('recipes/', views.RecipeList.as_view()),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name='recipe-detail'),
    # Get list of recipes from specific user
    # re_path supports regex expressions, path doesnt
    re_path(r'^users/(?P<user_pk>\d+)/recipes/?$', views.UserRecipesViewSet.as_view({'get': 'list'}), name='user-recipe'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)