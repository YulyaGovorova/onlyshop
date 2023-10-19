# coding: utf-8
from catalog.models import Product
from catalog.models import Category
Product.objects.all()
Category.objects.all()
Category.objects.create(category_name='Категория')
Product.objects.all(product_category='Категория', product_name='Название')
Category.objects.create(category_name='наименование')
st.save()
