import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Product


class LatestProductsFeed(Feed):
    title = 'My Products'
    link = reverse_lazy('product:product_list')
    description = 'New product of my blog.'

    def items(self):
        return Product.active_objects.all()[:5]

    def item_name(self, item):
        return item.name

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.description), 30)

    def item_pubdate(self, item):
        return item.updated_at