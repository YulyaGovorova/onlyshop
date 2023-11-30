import datetime
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='product/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='категория')
    cost = models.FloatField(verbose_name='цена')
    create_data = models.DateField(verbose_name='на удаление', default=datetime.date.today)

    def __str__(self):
        return f"{self.name}\nЦена: {self.cost}"

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    create_at = models.DateField(verbose_name='на удаление', default=datetime.date.today)

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)
