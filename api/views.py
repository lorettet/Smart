from django.shortcuts import render
from django.http import HttpResponseNotAllowed, JsonResponse
import api.services as serv
from api.errors import *
from api.models import *

# Create your views here.

def index(request):
    return HttpResponse('Hello, world! This is the Optifood api index.')

def login(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return JsonResponse(errorJson('require fields : username, password'))

    user = serv.login(email,password)
    print(user)
    if user is None:
        return JsonResponse(errorJson('Login ou mot de passs incorrect'))

    json = user.getJson()
    return JsonResponse(json)


def get_store_products(request, storeId):
    '''
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        store = request.POST['store']
    except KeyError:
        return JsonResponse(errorJson('require field : store'))
    '''

    products = serv.getStoreProducts(storeId)
    print(products)

    if products is None:
        return JsonResponse(errorJson('id de magasin inexistant'))


    json = {}
    json['store'] = storeId
    json['products'] = products

    return JsonResponse(json)

def get_stores_all(request):
    return JsonResponse(serv.getAllStores())
