from catalog.apps import CatalogConfig

from django.urls import path

from catalog.views import index, contact, product

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('product/<int:pk>', product, name='product')
]

