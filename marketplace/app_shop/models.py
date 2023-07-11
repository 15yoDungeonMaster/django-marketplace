from django.db import models
from django.db.models import Avg

from app_users.models import User


# Пути к media файлам
def category_image_directory_path(instance, filename: str) -> str:
    if instance.parent:
        return f'categories/category_{instance.parent.id}/images/{filename}'
    return f'categories/category_{instance.id}/images/{filename}'


def product_image_directory_path(instance, filename: str) -> str:
    return f'products/product_{instance.product_id}/images/{filename}'


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='title')
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to=category_image_directory_path, blank=True, null=True)
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='subcategories',
                               null=True,
                               blank=True,
                               db_index=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='price')
    quantity = models.PositiveSmallIntegerField(verbose_name='quantity')
    date = models.DateTimeField(verbose_name='created', auto_now=True)
    title = models.CharField(max_length=150, verbose_name='title')
    full_description = models.TextField(max_length=1000, verbose_name='description', blank=True)
    free_delivery = models.BooleanField(default=True, verbose_name='free delivery')
    available = models.BooleanField(default=True, verbose_name='available')
    discount = models.PositiveSmallIntegerField(default=0, verbose_name='discount')

    def __str__(self):
        return f'ID: {self.id} {self.title}'

    def short_description(self):
        return self.full_description[:50]

    def reviews_count(self):

        if not self.reviews:
            return 0
        reviews = self.reviews.count()
        return reviews

    def average_rating(self):
        avg_rating = self.reviews.aggregate(rating=Avg('rate'))
        return avg_rating['rating']

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to=product_image_directory_path, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    product = models.ManyToManyField(Product, related_name='tags', )

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(default=0)
    text = models.TextField(blank=True)
    date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'review by: {self.author.name}'


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('free', 'free delivery'),
        ('express', 'paid delivery'),
    ]
    PAYMENT_CHOICES = [
        ('online', 'online payment'),
        ('offline', 'offline payment')
    ]
    STATUS_CHOICES = [
        ('accepted', 'accepted order'),
        ('rejected', 'rejected order'),
        ('delivery', 'order on delivery'),
        ('delivered', 'order is already delivered'),
    ]

    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    delivery_type = models.CharField(max_length=10)
    payment_type = models.CharField(max_length=10)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='accepted')
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    products = models.JSONField()

    def __str__(self):
        return f'Order: {self.id}'
