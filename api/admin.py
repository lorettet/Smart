from django.contrib import admin

# Register your models here.

from .models import Client, Store, Product, ProductModel, Category, FidelityPoints, Transaction, TransactionProduct

admin.site.register(Client)
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(ProductModel)
admin.site.register(Product)
admin.site.register(FidelityPoints)
admin.site.register(Transaction)
admin.site.register(TransactionProduct)