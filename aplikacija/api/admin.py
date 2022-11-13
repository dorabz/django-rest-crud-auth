from django.contrib import admin

# Register your models here.

from api.models import Recipe

# register model Recipe to see it in admin page
admin.site.register(Recipe) 