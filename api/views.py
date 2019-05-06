from django.shortcuts import render
from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponse
import api.services as serv
from api.errors import *
from api.models import *
from django.views.decorators.http import require_http_methods

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
        pPoints = request.POST['product_points']
        pQuantity = request.POST['product_quantity']

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
        
        client_id = request.POST['client_id']
        points = request.POST['points']

    except KeyError:
        return JsonResponse(errorJson('require fields : user_id(in session), client_id, points'),status=400)

    creditSuccessfull = serv.creditClient(store_id,client_id,points)
    if creditSuccessfull is None:
        return HttpResponse('false')
    else:
        return HttpResponse('true')

'''
@require_http_methods(['POST'])
def generateQRCode():
    if(request.session['user_type']=='store'):
        return HttpResponse(errors.errorJson('Store not allowed'),status=400)
'''

@require_http_methods(['POST'])
def debit(request):
    if(request.session['user_type']=='client'):
        return HttpResponse(errors.errorJson('Client not allowed'),status=400)

    try:
        store_id = request.session['user_id']
        
        client_hash = request.POST['client_hash']
        products = json.loads(request.body)

    except KeyError:
        return JsonResponse(errorJson('require fields : user_id(in session), client_hash, products(JSON)'),status=400)

    debitSuccessfull = serv.debitClient(store_id,client_hash,products)
    if debitSuccessfull is None:
        return HttpResponse('false')
    else:
        return HttpResponse('true')
