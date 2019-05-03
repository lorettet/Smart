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

def getFidelityPoints(client_id,store_id):
    try:
        return FidelityPoints.objects.get(client=client_id,store=store_id).points
    except FidelityPoints.DoesNotExist:
        return 0

def getAllFidelityPoints(client_id):
    return {'points':[{'store':x.store.getJson(),'points':x.points} for x in list(FidelityPoints.objects.filter(client=client_id))]}


def getStoreProducts(store_id):
    try:
        s = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return None

    return [product.getJson() for product in Product.objects.filter(store=s)]