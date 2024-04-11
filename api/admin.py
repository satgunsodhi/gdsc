from django.contrib import admin

# Register your models here.

from .models import News, apiKey, Comment, Log

admin.site.register(News)
admin.site.register(apiKey)
admin.site.register(Comment)
admin.site.register(Log)