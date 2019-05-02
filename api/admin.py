from django.contrib import admin

# Register your models here.

from .models import Client, Store

admin.site.register(Client)
admin.site.register(Store)