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

def getStore(store_id):
    try:
        s = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return None

    return s.getJson()

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


def addProduct(pName,pDescription,pCategory,store_id,pPoints,pQuantity):
    try:
        store = Store.objects.get(id=store_id)
        p = Product.objects.create(pName,pDescription,pCategory,store,pPoints,pQuantity)
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


def creditClient(store_id,client_id,points):
    try:
        s = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return None
    
    try:
        c = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return None

    fp = FidelityPoints.objects.get_or_create(store=s,client=c)

    fp.points += points
    
    fp.save()

    return fp.points
    