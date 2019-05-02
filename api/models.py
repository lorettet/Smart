from django.db import models
from django import forms

# Create your models here.

class Store(models.Model):
    @classmethod
    def create(cls, name, email, password, lat, lon):
        store = cls(name=name, email=email, password=password, lat=lat, lon=lon)
        return store

    def __str__(self):
        return self.name + '('+self.email+')'

    def updateLatLon(self, lat, lon):
        self.__lat = lat
        self.__lon = lon
    
    name = models.CharField(max_length=30,null=False)
    email = models.CharField(max_length=50,null=False,unique=True)
    password = models.CharField(max_length=50,null=False)
    
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

class Client(models.Model):
    @classmethod
    def create(cls, firstname, lastname, email, password):
        client = cls(firstname=firstname, lastname=lastname, email=email, password=password)
        return client

    def updateFidelityPoints(self, points):
        self.__points.points = points

    def __str__(self):
        return self.firstname+' '+self.lastname+' ('+self.email+')'

    firstname = models.CharField(max_length=30,null=False)
    lastname = models.CharField(max_length=30,null=False)
    email = models.CharField(max_length=50,null=False,unique=True)
    password = models.CharField(max_length=50,null=False)

    points = models.ManyToManyField(Store, through='FidelityPoints')

class FidelityPoints(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    
class Category(models.Model):
    @classmethod
    def create(cls, name, description):
        client = cls(name=name, description=description)
        return client

    def __str__(self):
        return self.name+'('+self.description+')'

    name = models.CharField(max_length=30,null=False)
    description = models.CharField(max_length=100,null=False)

class Product(models.Model):
    @classmethod
    def create(cls, name, description, category, store):
        client = cls(name=name, description=description, category=category, store=store)
        return client

    def __str__(self):
        return self.name+'('+self.description+','+str(self.category)+','+str(self.store)+')'

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30,null=False)
    description = models.CharField(max_length=100,null=False)
    store = models.OneToOneField(
        Store,
        on_delete=models.CASCADE
    )

class ProductModel(models.Model):
    @classmethod
    def create(cls, name, description, category):
        client = cls(name=name, description=description, category=category)
        return client

    def __str__(self):
        return self.name+'('+self.description+','+str(self.category)+')'


    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=30,null=False)
    description = models.CharField(max_length=100,null=False)
