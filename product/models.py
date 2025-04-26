from django.db import models
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager


class CanadaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(country='CAN')


class UsaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(country='USA')


class MexicoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(country='MEX')
    

class ProductActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Product(models.Model):
    class Country(models.TextChoices):
        USA = 'USA', 'United States'
        CANADA = 'CAN', 'Canada'
        MEXICO = 'MEX', 'Mexico'

    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100, 
        unique_for_date='created_at'
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    country = models.CharField(
        max_length=3,
        choices=Country,
        default=Country.USA,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='product_products'
    )

    objects = models.Manager()              # Default manager
    canada_objects = CanadaManager()        # Custom manager for Canada
    usa_objects = UsaManager()              # Custom manager for USA
    mexico_objects = MexicoManager()        # Custom manager for Mexico
    active_objects = ProductActiveManager() # Custom manager for active products
    tags = TaggableManager()

    class Meta:
        ordering = ['-name']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'product:product_detail',
            args=[self.created_at.year, self.created_at.month, self.created_at.day, self.slug]
        )


class Comment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.product}'