from django.db import models

# Create your models here.

class User(models.Model):
    message = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)

class SignUp(models.Model):
    user_id = models.CharField(max_length=255, unique=True )