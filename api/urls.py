from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('store/all', views.get_stores_all, name='allStores'),
    path('me/<int:store_id>/points',views.getFidelityPoints, name='getFidelityPoints')
]
