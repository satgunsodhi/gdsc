from django.contrib import admin

# Register your models here.

from .models import News, apiKey

admin.site.register(News)
admin.site.register(apiKey)