from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Article(models.Model):
    title =  models.CharField(max_length=200)
    description= models.TextField()
    # required field
    slug = models.SlugField(max_length=100, unique=True)
    published =  models.DateTimeField(auto_now_add=True)
    # many to one: a user can add article and evey article is related to one user and a user can add multiple articles
    # https://docs.djangoproject.com/en/4.1/ref/contrib/auth/
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles') 

def __str__(self):
    return self.title