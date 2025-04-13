from django.urls import path, include
from api import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', include('products.urls')),
    path('users/', include('users.urls')),
]
