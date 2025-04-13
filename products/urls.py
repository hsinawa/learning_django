from django.urls import path
from products.views import * 

urlpatterns = [
    path('manage-product', ProductList.as_view(), name='create_product'),    #URL to fetch and add products
    path('fetch-all-products', ProductList.as_view(), name='fetch_all_products'),
    path('fetch-product/<int:product_id>', ParticularProduct.as_view(), name='fetch_product'),
    path('update-product/<int:product_id>', ParticularProduct.as_view(), name='update_product'),      
    path('delete-product/<int:product_id>', ParticularProduct.as_view(), name='delete_product'),     
   
]
