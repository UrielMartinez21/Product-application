from django.contrib import admin
from .models import Product, Comment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'country')
    search_fields = ('name', 'description')
    show_facets = admin.ShowFacets.ALWAYS       # to always show facets in the admin interface
    prepopulated_fields = {'slug': ('name',)}   # to auto-generate slug from name


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'created')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
