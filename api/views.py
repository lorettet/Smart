from django.shortcuts import render
from django.http import HttpResponseNotAllowed, JsonResponse
import api.services as serv
from api.errors import *

# Create your views here.

def index(request):
    return HttpResponse('Hello, wolrd!')

def login(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return JsonResponse(errorJson('require fields : username, password'))

    user = serv.login(email,password)
    if(user):
        json = user.getJson()
        type = type(user)
        if(type == Client):
            json['type'] = 'client'
        else if(type==Store):
            json['type'] = 'store'
        return JsonResponse(json)

    return JsonResponse(errorJson('Login ou mot de passs incorrect'))
