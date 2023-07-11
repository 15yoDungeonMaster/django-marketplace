from django.contrib import admin

from .models import Category, Product, ProductImage, Tag, Review, Order


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'title',

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductImagesInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductTagsInline(admin.StackedInline):
    model = Product.tags.through
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'title', 'short_description',
    inlines = [ProductImagesInline, ProductTagsInline]

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'name',

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = 'author',

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'id',
