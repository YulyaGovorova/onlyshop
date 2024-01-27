from catalog.apps import CatalogConfig
from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,  contact

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', contact, name='contacts'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='view_product'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('product/update/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
    path('product/product_item/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product_item'),
    path('product/product/delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),
]

