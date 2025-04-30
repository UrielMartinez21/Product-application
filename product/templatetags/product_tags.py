from django import template
from ..models import Product
from django.db.models import Count


register = template.Library()

@register.simple_tag
def total_products():
    return Product.active_objects.count()


@register.inclusion_tag('product/latest_products.html')
def show_latest_products(count=5):
    latest_products = Product.active_objects.order_by('-created_at')[:count]
    return {'latest_products': latest_products}


@register.simple_tag
def get_most_commented_products(count:int = 5):
    return Product.active_objects.annotate(total_comments= Count('comments')).order_by('-total_comments')[:count]