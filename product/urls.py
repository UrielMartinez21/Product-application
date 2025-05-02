from django.urls import path
from . import views
from .feeds import LatestProductsFeed


app_name = 'product'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('tag/<slug:tag_slug>/', views.product_list, name='product_list_by_tag'),

    # path('', views.ProductListView.as_view(), name='product_list'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:product>/',
        views.product_detail,
        name='product_detail'
    ),
    path('<int:product_id>/share/', views.product_share, name='product_share'),
    path(
        '<int:product_id>/comment/',
        views.product_comment,
        name='product_comment'
    ),
    # Feeds
    path('feeds/', LatestProductsFeed(), name='product_feed'),
    path('search/', views.post_search, name='post_search'),
]