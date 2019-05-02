from django.db import models

# Create your models here.

class User(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    id = models.AutoField(primary_key=True)
