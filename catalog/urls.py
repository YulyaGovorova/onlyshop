from catalog.views import index, format

from django.urls import path

urlpatterns = [
    path('', index),
    path('contacts/', format)
]

