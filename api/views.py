from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

def index(request):
    return HttpResponse('Hello, world! This is the Optifood api index.')

def login(request):
    pass



def get_stores_all(request):
    stores = User.objects.filter(type="store")
    stores_list = list(stores)  # important: convert the QuerySet to a list object
    return JsonResponse(users_list, safe=False)

# def get_stores(request):