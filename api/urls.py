from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('store/all', views.get_stores_all, name='getAllStores'),
    path('store/<int:store_id>', views.get_store_infos, name='getStoreInfos'),
    path('category/all', views.get_categories_all, name='getAllCategories'),
    path('me/points',views.getAllFidelityPoints, name='getAllFidelityPoints'),
    path('me/points/<int:store_id>',views.getFidelityPoints, name='getFidelityPoints'),
    path('me/client/<int:client_id>/points',views.getPointsForClient, name='getPointsForClient'),
    path('products/<int:storeId>', views.get_store_products, name='getStoreProducts'),
    path('me/products/add', views.add_product_to_store, name='addProductToStore'),
    path('me/products/update', views.update_product, name='updateProduct'),
    path('me/products/remove', views.remove_product_from_store, name='removeProductFromStore'),
    path('transaction/credit', views.credit, name='credit'),
    path('transaction/debit', views.debit, name='debit'),
    path('me/qrcode', views.generateQRCode, name='generateQRCode'),
]
