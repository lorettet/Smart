from django.db import models
from django import forms

# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=50,null=False,unique=True)
    password = models.CharField(max_length=50,null=False)
    class Meta:
        abstract = True

class Client(User):
    @classmethod
    def create(cls, firstname, lastname, email, password):
        client = cls(firstname=firstname, lastname=lastname, email=email, password=password)
        return client

    def __str__(self):
        return self.firstname+' '+self.lastname+' ('+self.email+')'

    def getJson(self):
        json = {'type':'client',
                'firstname':self.firstname,
                'lastname':self.lastname,
                'email':self.email,
                }
        return json



    firstname = models.CharField(max_length=30,null=False)
    lastname = models.CharField(max_length=30,null=False)

class Store(User):
    def __init(self):
        User.__init__(self)

    @classmethod
    def create(cls, name, email, password, lat, long):
        store = cls(name=name, email=email, password=password, lat=lat, long=long)
        return store

    def __str__(self):
        return self.name + '('+self.email+')'

    def getJson(self):
        json = {'type':'client',
                'name':self.name,
                'email':self.email,
                }
        return json

    name = models.CharField(max_length=30,null=False)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)

'''
class Product(models.Model):
    category
    name
    store =

class ProductModel(models.Model)
    category
    name
'''
