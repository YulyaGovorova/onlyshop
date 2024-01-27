from config.settings import CACHE_ENABLED
from django.core.cache import cache
from catalog.models import Category


def get_categories():
    if CACHE_ENABLED == 'True':
        key = f'categories_list'
        categories = cache.get(key)
        if categories is None:
            categories = Category.objects.all()
            cache.set(key, categories)
    else:
        categories = Category.objects.all()

    return categories