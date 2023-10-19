import json

from django.core.management import BaseCommand

from catalog.models import Category


class Command(BaseCommand):
    def handle(self, *args, **option):
        Category.objects.all().delete()

        with open('data.json', 'rt', encoding="utf-8") as file:
            category_for_create = []
            for item in json.load(file):
                category_for_create.append(Category(item['pk'], **item['fields']))

        Category.objects.bulk_create(category_for_create)
