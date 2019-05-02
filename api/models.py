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

    firstname = models.CharField(max_length=30,null=False)
    lastname = models.CharField(max_length=30,null=False)        

class Store(User):
    @classmethod
    def create(cls, name, email, password):
        store = cls(name=name, email=email, password=password)
        return store

    def __str__(self):
        return self.name + '('+self.email+')'
    
    name = models.CharField(max_length=30,null=False)
    
'''
class Product(models.Model):
    category
    name
    store = 

class ProductModel(models.Model)
    category
    name
'''