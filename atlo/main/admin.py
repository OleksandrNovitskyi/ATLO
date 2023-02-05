from django.contrib import admin

from .models import Traffic, Results, Speed, Profile

admin.site.register(Traffic)

admin.site.register(Results)

admin.site.register(Speed)

admin.site.register(Profile)
