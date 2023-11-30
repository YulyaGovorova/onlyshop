from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'slug', 'preview', 'created_at', 'publication', 'views_count'
    )
    list_filter = ('publication',)
    search_fields = ('title', 'created_at',)