from django import template
from ..models import Product
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe


register = template.Library()

# To create a custom template tag

@register.simple_tag
def total_products():
    """ This function returns a value """

    return Product.active_objects.count()


@register.inclusion_tag('product/latest_products.html')
def show_latest_products(count=5):
    """ This function returns a template """

    latest_products = Product.active_objects.order_by('-created_at')[:count]
    return {'latest_products': latest_products}


@register.simple_tag
def get_most_commented_products(count:int = 5):
    """ This function returns a queryset """

    return Product.active_objects.annotate(total_comments= Count('comments')).order_by('-total_comments')[:count]


# To create a custom filter

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))