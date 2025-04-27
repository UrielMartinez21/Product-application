from django import template
from ..models import Product


register = template.Library()

@register.simple_tag
def total_products():
    return Product.active_objects.count()