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
def getFidelityPoints(request,store_id):
    if(request.session['user_type']=='store'):
        return HttpResponse(errors.errorJson('Store not allowed'),status=400)
    return HttpResponse(serv.getFidelityPoints(request.session['user_id'],store_id))
