from django.db import models
from django import forms
import datetime

# Create your models here.

class Store(models.Model):
    @classmethod
    def create(cls, name, email, password, city, code, address, lat, lon):
        store = cls(name=name, email=email, password=password, city=city, code=code, address=address, lat=lat, lon=lon)
        return store

    def __str__(self):
        return self.name + ' ('+self.email+', '+self.city+', '+self.code+', '+self.address+', '+str(self.lat)+' '+str(self.lon)+')'

    def getJson(self):
        json = {
                'type':'store',
                'id':self.id,
                'name':self.name,
                'email':self.email,
                'city':self.city,
                'code':self.code,
                'address':self.address,
                'lat':self.lat,
                'lon':self.lon,
                }
        return json

    name = models.CharField(max_length=30,null=False)
    email = models.CharField(max_length=50,null=False,unique=True)
    password = models.CharField(max_length=50,null=False)
    city = models.CharField(max_length=20,null=False)
    code = models.CharField(max_length=10,null=False)
    address = models.CharField(max_length=40,null=False)
    lat = models.DecimalField(max_digits=15, decimal_places=6)
    lon = models.DecimalField(max_digits=15, decimal_places=6)

class Client(models.Model):
    @classmethod
    def create(cls, firstname, lastname, email, password):
        client = cls(firstname=firstname, lastname=lastname, email=email, password=password)
        return client

    def __str__(self):
        return self.firstname+' '+self.lastname+' ('+self.email+')'

    def getJson(self):
        json = {
                'type':'client',
                'id':self.id,
                'firstname':self.firstname,
                'lastname':self.lastname,
                'email':self.email,
                }
        return json

    firstname = models.CharField(max_length=30,null=False)
    lastname = models.CharField(max_length=30,null=False)
    email = models.CharField(max_length=50,null=False,unique=True)
    password = models.CharField(max_length=50,null=False)
    points = models.ManyToManyField(Store, through='FidelityPoints')
    code = models.CharField(max_length=70,null=True)
    generatedOn = models.DateTimeField(null=True)

class FidelityPoints(models.Model):
    @classmethod
    def create(cls, client, store, points):
        fidelityPoints = cls(client=client, store=store, points=points)
        return fidelityPoints

    def __str__(self):
        return str(self.client)+' ('+self.store.name+' : '+str(self.points)+')'

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

class Category(models.Model):
    @classmethod
    def create(cls, name, description):
        category = cls(name=name, description=description)
        return category

    def __str__(self):
        return self.name+' ('+self.description+')'

    def getJson(self):
        json = {
                'id':self.id,
                'name':self.name,
                'description':self.description,
                }
        return json

    name = models.CharField(max_length=30,null=False)
    description = models.CharField(max_length=100,null=False)

class Product(models.Model):
    @classmethod
    def create(cls, name, description, category, store, points, quantity):
        product = cls(name=name, description=description, category=category, store=store, points=points, quantity=quantity)
        return product

    def __str__(self):
        return self.name+' ('+self.description+', '+self.category.name+', '+str(self.store)+', '+str(self.points)+', '+str(self.quantity)+')'

    def getJson(self):
        json = {
                'id':self.id,
                'name':self.name,
                'description':self.description,
                'category':self.category.name,
                'points':self.points,
                'quantity':self.quantity,
                }
        return json

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=30,null=False)
    description = models.CharField(max_length=100,null=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

class ProductModel(models.Model):
    @classmethod
    def create(cls, name, description, category):
        productModel = cls(name=name, description=description, category=category)
        return productModel

    def __str__(self):
        return self.name+' ('+self.description+', '+self.category.name+')'


    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=30,null=False)
    description = models.CharField(max_length=100,null=False)

class Transaction(models.Model):
    @classmethod
    def create(cls, client, store, validatedOn):
        transaction = cls(client=client, store=store, validatedOn=validatedOn)
        return transaction

    def __str__(self):
        return str(self.client)+' ('+self.store.name+' : '+str(self.validatedOn)+')'

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    validatedOn = models.DateTimeField(null=True)
    products = models.ManyToManyField(Product, through='TransactionProduct')

class TransactionProduct(models.Model):
    @classmethod
    def create(cls, transaction, product, quantity):
        transactionProducts = cls(transaction=transaction, product=product, quantity=quantity)
        return transactionProducts

    def __str__(self):
        return str(self.transaction)+' ('+self.product.name+' : '+str(self.quantity)+')'

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)