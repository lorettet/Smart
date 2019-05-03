from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('store/all', views.get_stores_all, name='allStores'),
    path('products/<int:storeId>', views.get_store_products, name='storeProducts'),
]
