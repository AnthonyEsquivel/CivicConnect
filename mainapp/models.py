from django.db import models
from django.contrib.auth.models import User, AnonymousUser


# Create your models here.


class Tags(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    location = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True) 
    location = models.CharField(max_length=200, blank=True)

class Template(models.Model):
    temp_name = models.CharField(max_length=200)
    temp_description = models.TextField()
    temp_text = models.TextField()
    tags = models.ManyToManyField(Tags)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.temp_text
