from django.contrib import admin
from .models import *
from django.apps import apps
from django.contrib.auth.models import Group

admin.site.unregister(Group)
for model in apps.get_app_config('api').models.values():
    admin.site.register(model)