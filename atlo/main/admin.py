from django.contrib import admin

from .models import Traffic, Results, OtherParam, Profile

admin.site.register(Traffic)

admin.site.register(Results)

admin.site.register(OtherParam)

admin.site.register(Profile)
