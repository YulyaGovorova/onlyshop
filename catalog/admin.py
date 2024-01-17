from django.contrib import admin

from catalog.models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description',)
    search_fields = ('name', 'description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'cost', 'category',)
    list_filter = ('category', 'product_is_publicated',)
    search_fields = ('name', 'description',)

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'version_product', 'version_name', 'version_number', 'version_is_active',)
    list_filter = ('version_is_active',)
    search_fields = ('version_name',)