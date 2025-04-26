from django.shortcuts import render, get_object_or_404
from .forms import EmailProductFrom, CommentForm
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

# To class-based views:
from django.views.generic import ListView


def product_list(request, tag_slug=None):
    product_list = Product.active_objects.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        product_list = product_list.filter(tags__in=[tag])

    paginator = Paginator(product_list, 3)      # Show 3 products per page
    page_number = request.GET.get('page', 1)    # Get the page number from the request
    try:
        products = paginator.page(page_number)  # Get the products for the current page, it's a Page object
    except PageNotAnInteger:                    # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page of results.

    return render(request, 'product/product_list.html', {'products': products, 'tag': tag})


class ProductListView(ListView):
    """Alternative way using class-based view"""
    queryset = Product.active_objects.all()
    context_object_name = 'products'
    paginate_by = 3
    template_name = 'product/product_list.html'


def product_detail(request, year, month, day, product):
    product = get_object_or_404(
        Product,
        slug=product,
        created_at__year=year,
        created_at__month=month,
        created_at__day=day,
    )

    comments = product.comments.filter(active=True)                 # Get active comments for this product
    form = CommentForm()                                            # Create a new comment form

    # List of similar products
    product_tags_ids = product.tags.values_list('id', flat=True)    # Get the a list tags of the product

    similar_products = Product.active_objects.filter(
        tags__in=product_tags_ids                                   # Get similar products
    ).exclude(id = product.id)                                      # Exclude the current product

    similar_products = similar_products.annotate(
        same_tags = Count('tags')
    ).order_by('-same_tags', 'created_at')[:4]                      # Order by the number of same tags and limit to 4

    return render(
        request, 
        'product/product_detail.html', 
        {'product': product, 'comments': comments, 'form': form, 'similar_products': similar_products}
    )


def product_share(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailProductFrom(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            product_url = request.build_absolute_uri(product.get_absolute_url())
            subject = (
                f"{cd['name']}"
                f" recommends you read {product.name}"
            )
            message = f"Read {product.name} at {product_url}\n\n{cd['name']}'s comments: {cd['comment']}"
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']],
            )
            sent = True
    else:
        form = EmailProductFrom()

    return render(request, 'product/share.html', {'product': product, 'form': form, 'sent': sent})


@require_POST
def product_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.product = product
        comment.save()

    return render(request, 'product/comment.html', {'product': product, 'form': form, 'comment': comment})
