from django.db import models
from django import forms

# Create your models here.

class User(models.Model):
    @classmethod
    def create(cls, firstname,lastname,email,password):
        user = cls(firstname=firstname, lastname=lastname, email=email, password=password)
        return user

    def __str__(self):
        return self.firstname+' '+self.lastname+' ('+self.email+')'

    def getJson(self):
        json = {'firstname':self.firstname,
                'lastname':self.lastname,
                'email':self.email,
                }
        return json



    firstname = models.CharField(max_length=30,null=False)
    lastname = models.CharField(max_length=30,null=False)
    email = models.CharField(max_length=50,null=False,unique=True)
    password = models.CharField(max_length=50,null=False)
