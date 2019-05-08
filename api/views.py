from django.shortcuts import render
from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponse
import api.services as serv
from api.errors import *
from api.models import *
from django.views.decorators.http import require_http_methods
import json


# Create your views here.

def index(request):
    return HttpResponse('Hello, world! This is the Optifood api index.')

@require_http_methods(['POST'])
def login(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return JsonResponse(errorJson('require fields : username, password'),status=400)

    user = serv.login(email,password)
    if user is None:
        return HttpResponse('false')

    request.session['user_id']=user.id
    json = user.getJson()
    request.session['user_type']=json['type']
    return JsonResponse(json)

@require_http_methods(['POST'])
def get_store_products(request, storeId):

    products = serv.getStoreProducts(storeId)
    print(products)

    if products is None:
        return JsonResponse(errorJson('id de magasin inexistant'))

    json = {}
    json['store'] = storeId
    json['products'] = products

    return JsonResponse(json)

@require_http_methods(['POST'])
def get_stores_all(request):
    return JsonResponse(serv.getAllStores())

@require_http_methods(['POST'])
def get_store_infos(request,store_id):
    if(request.session['user_type']=='store'):
        return HttpResponse(errors.errorJson('Store not allowed'),status=400)

    store = serv.getStore(store_id)
    if store is None:
        return JsonResponse(errorJson('id de magasin inexistant'))
    products = serv.getStoreProducts(store_id)
    fp = serv.getFidelityPoints(request.session['user_id'],store_id)

    json = {}
    json['store'] = store
    json['products'] = products
    json['fidelityPoints'] = fp

    return JsonResponse(json)


@require_http_methods(['POST'])
def get_categories_all(request):
    return JsonResponse(serv.getAllCategories())


@require_http_methods(['POST'])
def getFidelityPoints(request,store_id):
    if(request.session['user_type']=='store'):
        return HttpResponse(errors.errorJson('Store not allowed'),status=400)
    return HttpResponse(serv.getFidelityPoints(request.session['user_id'],store_id))

@require_http_methods(['POST'])
def getAllFidelityPoints(request):
    if(request.session['user_type']=='store'):
        return HttpResponse(errors.errorJson('Store not allowed'),status=400)
    return JsonResponse(serv.getAllFidelityPoints(request.session['user_id']))


@require_http_methods(['POST'])
def add_product_to_store(request):
    if(request.session['user_type']=='client'):
        return HttpResponse(errors.errorJson('Client not allowed'),status=400)

    try:
        store_id = request.session['user_id']

        pName = request.POST['product_name']
        pDescription = request.POST['product_description']
        pCategory = request.POST['product_category']
        pPoints = int(request.POST['product_points'])
        pQuantity = int(request.POST['product_quantity'])

    except KeyError:
        return JsonResponse(errorJson('require fields : user_id(in session), product_name, product_description, product_category, product_points, product_quantity'),status=400)

    product = serv.addProduct(pName,pDescription,pCategory,store_id,pPoints,pQuantity)
    if product is None:
        return HttpResponse('false')

    json = product.getJson()
    return JsonResponse(json)


@require_http_methods(['POST'])
def update_product(request):
    if(request.session['user_type']=='client'):
        return HttpResponse(errors.errorJson('Client not allowed'),status=400)

    try:
        store_id = request.session['user_id']

        product_id = request.POST['product_id']
        pName = request.POST['product_name']
        pDescription = request.POST['product_description']
        pCategory = request.POST['product_category']
        pPoints = request.POST['product_points']
        pQuantity = request.POST['product_quantity']

    except KeyError:
        return JsonResponse(errorJson('require fields : user_id(in session), product_id, product_name, product_description, product_category, product_points, product_quantity'),status=400)

    product = serv.updateProduct(product_id,pName,pDescription,pCategory,store_id,pPoints,pQuantity)
    if product is None:
        return HttpResponse('false')

    json = product.getJson()
    return JsonResponse(json)


@require_http_methods(['POST'])
def remove_product_from_store(request):
    if(request.session['user_type']=='client'):
        return HttpResponse(errors.errorJson('Client not allowed'),status=400)

    try:
        store_id = request.session['user_id']

        product_id = request.POST['product_id']

    except KeyError:
        return JsonResponse(errorJson('require fields : user_id(in session), product_id'),status=400)

    deletion = serv.removeProduct(product_id,store_id)
    if deletion is None:
        return HttpResponse('false')

    json = deletion.getJson()
    return JsonResponse(json)


@require_http_methods(['POST'])
def credit(request):
    if(request.session['user_type']=='client'):
        return HttpResponse(errors.errorJson('Client not allowed'),status=400)

    try:
        store_id = request.session['user_id']

        client_hash = request.POST['client_hash']

    except KeyError:
        return JsonResponse(errorJson('require fields : user_id(in session), client_hash'),status=400)

    creditSuccessfull = serv.creditClient(store_id,client_hash)
    return HttpResponse(creditSuccessfull)

@require_http_methods(['POST'])
def generateQRCode(request):
    if(request.session['user_type']=='store'):
        return HttpResponse(errors.errorJson('Store not allowed'),status=400)
    try:
        rep = serv.generateQRCode(request.session['user_id'])
    except KeyError:
        return JsonResponse(errorJson('require fields : user_id(in session)'),status=400)

    if rep == None:
        return HttpResponse('false')
    return JsonResponse(rep)

@require_http_methods(['POST'])
def debit(request):
    if(request.session['user_type']=='client'):
        return HttpResponse(errors.errorJson('Client not allowed'),status=400)

    try:
        store_id = request.session['user_id']

        #client_hash = request.POST['client_hash']
        #transaction = json.loads(request.body)
        transaction = json.loads(request.POST['json'])

    except KeyError:
        return JsonResponse(errorJson('require fields : user_id(in session), json(JSON)'),status=400)

    debitSuccessfull = serv.debitClient(store_id,transaction)
    if debitSuccessfull is None:
        return JsonResponse(errorJson('Erreur : debit impossible'))
    else:
        return JsonResponse(successJson())

@require_http_methods(['POST'])
def getPointsForClient(request):
    if(request.session['user_type']=='client'):
        return HttpResponse(errorJson('Client not allowed'),status=400)

    try:
        store_id = request.session['user_id']
        hash = request.POST['hash']
    except KeyError:
        return JsonResponse(errorJson('Need to login'),status=400)
    points = serv.getPointsForClient(store_id,hash)
    if points is None:
        return HttpResponse('false')
    return HttpResponse(points)

@require_http_methods(['POST'])
def getAllProductModels(request):
    return JsonResponse(serv.getAllProductModels())


@require_http_methods(['POST'])
def getPurchaseRecords(request):
    if(request.session['user_type']=='Store'):
        return HttpResponse(errors.errorJson('Store not allowed'),status=400)

    return JsonResponse(serv.getPurchaseRecords(request.session['user_id']))

@require_http_methods(['POST'])
def updateInfo(request):
    if(request.session['user_type']=='store'):
        store_id = request.session['user_id']
        givenPoints = request.POST['store_givenPoints']
        saleStart = request.POST['store_saleStart']
        saleEnd = request.POST['store_saleEnd']

        store = serv.updateStoreInfo(store_id,givenPoints,saleStart,saleEnd)
        if store:
            rep = successJson('Vos informations ont bien été mises à jour')
            rep['store'] = store.getJson()
            return JsonResponse(rep)
        else:
            return JsonResponse(errorJson())

    elif(request.session['user_type']=='client'):

        client_id = request.session['user_id']
        firstname = request.POST['client_firstname']
        lastname = request.POST['client_lastname']
        password = request.POST['client_password']
        email = request.POST['client_email']

        client = serv.updateClientInfo(client_id,firstname,lastname,password,email)
        if client:
            rep = successJson('Vos informations ont bien été mises à jour')
            rep['client'] = client.getJson()
            return JsonResponse(rep)
        else:
            return JsonResponse(errorJson())
    
    else:
        return HttpResponse(errors.errorJson('User type not allowed'),status=400)
