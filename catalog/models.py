
import datetime
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='наименование')
    product_description = models.TextField(verbose_name='описание')
    product_preview = models.ImageField(upload_to='product/', verbose_name='изображение', **NULLABLE)
    product_category = models.CharField(max_length=100, verbose_name='категория')
    product_cost = models.FloatField(verbose_name='цена')
    product_data_created = models.DateField(verbose_name='создан', default=datetime.date.today)
    product_last_data_change = models.DateField(verbose_name='последнее изменение', default=datetime.date.today)
    product_data_at_created = models.DateField(verbose_name='на удаление', default=datetime.date.today)

    def __str__(self):
        return f"{self.product_name}\nЦена: {self.product_cost}"

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('product_name',)


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='наименование')
    category_description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f"{self.category_name} {self.category_description}"

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('category_name',)
