from api.models import *

def login(email, password):
    try:
        u = Client.objects.get(email=email, password=password)
        return u
    except Client.DoesNotExist:
        pass
    try:
        u = Store.objects.get(email=email, password=password)
        return u
    except Store.DoesNotExist:
        return None

def getAllStores():
    return {'stores':[store.getJson() for store in Store.objects.all()]}

def getStoreProducts(store):
    try:
        s = Store.objects.get(id=store)
        return [product.getJson() for product in Product.objects.filter(store=s)]
    except Store.DoesNotExist:
        return None

    


    