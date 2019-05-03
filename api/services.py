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


def createUser(firstname,lastname,email,password):
    u = User.create(firstname,lastname,email,password)
    u.save()

def getAllStores():
    return {'stores':[store.getJson() for store in Store.objects.all()]}
