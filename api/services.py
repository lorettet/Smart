from api.models import *
from datetime import datetime
from random import random
from hashlib import sha1
import struct

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

def getStore(store_id):
    try:
        s = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return None

    return s.getJson()

def getAllStores():
    return {'stores':[store.getJson() for store in Store.objects.all()]}

def getAllCategories():
    return {'categories':[category.getJson() for category in Category.objects.all()]}

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


def addProduct(pName,pDescription,pCategory,store_id,pPoints,pQuantity):
    try:
        store = Store.objects.get(id=store_id)
        c = Category.objects.get(name=pCategory)
        p = Product.objects.create(name=pName,description=pDescription,category=c,store=store,points=pPoints,quantity=pQuantity)
        p.save()
    except:
        return None

    return p


def updateProduct(product_id,pName,pDescription,pCategory,store_id,pPoints,pQuantity):
    try:
        p = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None

    if(p.store.id == store_id):
        p.name = pName
        p.description = pDescription
        try:
            c = Category.objects.get(name=pCategory)
        except Category.DoesNotExist:
            return None
        p.category = c
        p.points = pPoints
        p.quantity = pQuantity

        p.save()
    else:
        return None

    return p


def removeProduct(product_id,store_id):
    try:
        p = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None

    if(p.store.id == store_id):
        return p.delete()
    else:
        return None


def creditClient(store_id,client_id):
    try:
        s = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return None

    try:
        c = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return None

    fp = FidelityPoints.objects.get_or_create(store=s,client=c)

    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    t = Transaction.objects.filter(client=c, store=s, generatedOn__range=(today_min, today_max))

    if not t:
        fp.points += s.givenPoints
        fp.save()
        return fp.points
    else:
        return None




def debitClient(store_id,client_hash,products):
    try:
        s = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return None

    try:
        c = Client.objects.filter(code=client_hash, generatedOn__gte=(datetime.datetime.now()-datetime.timedelta(minutes=10)))
    except Client.DoesNotExist:
        return None

    transactionPoints = 0
    for p in products:
        pId = p['product']
        pQuantity = p['quantity']

        product = Product.objects.get(id=pId)

        transactionPoints += (product.points * pQuantity)

    try:
        fp = FidelityPoints.objects.get(store=s,client=c)
    except:
        return None

    if(transactionPoints <= fp.points):
        validatedOn = datetime.now()

        try:
            t = Transaction.objects.create(client=c, store=s, validatedOn=validatedOn)

        
            for p in products:
                transactionProduct = p['product']
                transactionQuantity = p['quantity']
                tp = TransactionProduct.objects.create(transaction=transaction, product=product, quantity=quantity)
        
        except:
            return None

        fp.points -= transactionPoints
        
    else:
        return None

    return t


def generateQRCode(client_id):
    try:
        client = Client.objects.get(id=client_id)
    except Store.DoesNotExist:
        return None

    date=datetime.timestamp(datetime.now())+10*1000*60
    m = sha1()
    m.update(struct.pack('f',random()))
    hash = m.hexdigest()

    code = hash+':'+str(date)
    client.code = hash
    client.generatedOn = datetime.fromtimestamp(date)
    client.save()

    return code

def getPointsForClient(store_id,client_id):
    try:
        points = FidelityPoints.objects.get(client=client_id, store=store_id)
    except FidelityPoints.DoesNotExist:
        return 0
    return points.points
