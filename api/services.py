from api.models import *
from datetime import datetime, date, time, timedelta
from django.conf import settings
from django.utils.timezone import make_aware
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

    fp, created = FidelityPoints.objects.get_or_create(store=s,client=c)

    settings.TIME_ZONE        

    today_min = make_aware(datetime.combine(date.today(), time.min))
    print(today_min)
    today_max = make_aware(datetime.combine(date.today(), time.max))
    print(today_max)
    
    print(fp.lastTimeCredited)
    if((fp.lastTimeCredited is not None) and (fp.lastTimeCredited>=today_min and fp.lastTimeCredited<=today_max)):
        return None
    else:
        fp.points += s.givenPoints
        fp.lastTimeCredited = make_aware(datetime.now())
        fp.save()
        return fp.points


def debitClient(store_id,transaction):
    try:
        s = Store.objects.get(id=store_id)
        print(s)
    except Store.DoesNotExist:
        print("no store found")
        return None

    client_hash = transaction['client_hash']

    settings.TIME_ZONE        
    debitTime = make_aware(datetime.now())

    clientList = Client.objects.filter(code=client_hash, generatedOn__gte=(debitTime-timedelta(minutes=10)))
    if not clientList:
        print("no client found")
        return None
    else:
        c = clientList[0]
        print(c)

    products = transaction['products']

    transactionPoints = 0
    for p in products:
        pId = p['id']
        pQuantity = p['quantity']

        product = Product.objects.get(id=pId)
        print(product)
        print(product.points)
        print(pQuantity)

        transactionPoints += (product.points * pQuantity)

    print(transactionPoints)

    try:
        fp = FidelityPoints.objects.get(store=s,client=c)
        print(fp)
    except:
        print("fp not found")
        return None

    if(transactionPoints <= fp.points):
        #validatedOn = datetime.now()
        settings.TIME_ZONE        
        validatedOn = make_aware(datetime.now())

        try:
            t = Transaction.objects.create(client=c, store=s, validatedOn=validatedOn)        
            t.save()
        except:
            print("couldn't create transaction")
            return None

        try:
            for p in products:
                transactionProductId = p['id']

                transactionProduct = Product.objects.get(id=pId)
                transactionQuantity = p['quantity']
                tp = TransactionProduct.objects.create(transaction=t, product=transactionProduct, quantity=transactionQuantity)
                tp.save()
        except:
            print("couldn't create transactionProducts")
            return None

        fp.points -= transactionPoints
        fp.save()

        c.code = None
        c.save()
        
    else:
        print("not enough points")
        return None

    return t


def generateQRCode(client_id):
    try:
        client = Client.objects.get(id=client_id)
    except Store.DoesNotExist:
        return None

    settings.TIME_ZONE        
    genTime = make_aware(datetime.now())

    date=datetime.timestamp(genTime)
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
