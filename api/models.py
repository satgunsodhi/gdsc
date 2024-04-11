from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    date = models.DateTimeField()
    views = models.BigIntegerField()
    def __str__(self):
        return self.title
    
class apiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=256)
    def __str__(self) -> str:
        return self.api_key