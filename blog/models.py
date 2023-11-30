from django.db import models
from django.utils.text import slugify
import datetime

NULLABLE = {'null': True, 'blank': True}

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое', **NULLABLE)
    slug = models.CharField(max_length=100, verbose_name='slug')
    preview = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    created_at = models.DateField(verbose_name='Создан', default=datetime.date.today)
    publication = models.BooleanField(verbose_name='опубликован', default=False)
    views_count = models.BigIntegerField(verbose_name='количество просмотров', default=0)

    def __str__(self):
        return f'{self.title}\nСоздан: {self.created_at}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        ordering = ('title',)
