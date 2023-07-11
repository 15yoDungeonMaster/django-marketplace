from django.db.models import Avg
from rest_framework import serializers

from .models import Category, Product, Tag, Order, Review


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField(method_name='get_subcategories')
    image = serializers.SerializerMethodField(method_name='get_image')

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories')

    def get_subcategories(self, obj):
        subcategories = [
            {
                'id': subcategory.id,
                'title': subcategory.title,
                'image': {
                    'src': (subcategory.image.url or ''),
                    'alt': subcategory.title
                }
            }
            for subcategory in obj.subcategories.all()
        ]
        return subcategories

    def get_image(self, obj):
        return {'src': (obj.image.url or ''), 'alt': obj.title}


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    tags = serializers.SerializerMethodField(method_name='get_tags')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    rating = serializers.SerializerMethodField(method_name='get_rating')
    salePrice = serializers.SerializerMethodField(method_name='get_sale_price')

    class Meta:
        model = Product
        fields = ('id',
                  'category',
                  'price',
                  'salePrice',
                  'count',
                  'date',
                  'title',
                  'description',
                  'freeDelivery',
                  'images',
                  'tags',
                  'reviews',
                  'rating')
        extra_kwargs = {
            'freeDelivery': {'source': 'free_delivery'},
            'description': {'source': 'short_description'},
            'count': {'source': 'quantity'},
        }

    def get_images(self, obj):
        images = [
            {
                'src': product_image.image.url or '',
                'alt': product_image.product.title
            }
            for product_image in obj.images.all()
        ]

        return images

    def get_tags(self, obj):
        tags = [
            {
                'id': tag.id,
                'name': tag.name,
            }
            for tag in obj.tags.all()
        ]
        return tags

    def get_reviews(self, obj):
        if not obj.reviews:
            return 0
        reviews = obj.reviews.count()
        return reviews

    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(rating=Avg('rate'))
        return avg_rating['rating']

    def get_sale_price(self, obj):
        if not obj.discount:
            return None
        return round(obj.price - obj.price / 100 * obj.discount, 2)


class ReviewSerializer(serializers.ModelSerializer):
    # author = serializers.SerializerMethodField(method_name='get_author', read_only=True)
    # email = serializers.SerializerMethodField(method_name='get_email', read_only=True)

    class Meta:
        model = Review
        fields = (
            # 'author', 'email',
            'text', 'rate', 'date'
        )
        # extra_kwargs = {
        #     'author': {'source': 'author.profile.fullName'},
        #     'email': {'source': 'author.profile.email'},
        # }

    def get_author(self, obj):
        return obj.author.profile.fullName


class ProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    tags = serializers.SerializerMethodField(method_name='get_tags')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    rating = serializers.SerializerMethodField(method_name='get_rating')
    salePrice = serializers.SerializerMethodField(method_name='get_sale_price')
    fullDescription = serializers.SerializerMethodField(method_name='get_full_description')
    specifications = serializers.SerializerMethodField(method_name='get_specifications')

    class Meta:
        model = Product
        fields = ('id',
                  'category',
                  'price',
                  'salePrice',
                  'count',
                  'date',
                  'title',
                  'description',
                  'fullDescription',
                  'freeDelivery',
                  'images',
                  'tags',
                  'reviews',
                  'specifications',
                  'rating')
        extra_kwargs = {
            'freeDelivery': {'source': 'free_delivery'},
            'description': {'source': 'short_description'},
            'count': {'source': 'quantity'},
        }

    def get_images(self, obj):
        images = [
            {
                'src': product_image.image.url or '',
                'alt': product_image.product.title
            }
            for product_image in obj.images.all()
        ]

        return images

    def get_tags(self, obj):
        tags = [
            {
                'id': tag.id,
                'name': tag.name,
            }
            for tag in obj.tags.all()
        ]
        return tags

    def get_reviews(self, obj):
        reviews = [
            {
                'author': review.author.profile.fullName,
                'email': review.author.profile.email,
                'text': review.text,
                'rate': review.rate,
                'date': review.date
            }
            for review in obj.reviews.all()
        ]
        return reviews

    def get_sale_price(self, obj):
        if not obj.discount:
            return None
        return round(obj.price - obj.price / 100 * obj.discount, 2)

    def get_full_description(self, obj):
        return obj.full_description

    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(rating=Avg('rate'))
        return avg_rating['rating']

    def get_specifications(self, obj):
        return [{
            "name": "Size",
            "value": "XL"
        }]


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name',)


class OrderSerializer(serializers.ModelSerializer):
    createdAt = serializers.SerializerMethodField(method_name='get_createdAt')
    fullName = serializers.SerializerMethodField(method_name='get_fullName')
    email = serializers.SerializerMethodField(method_name='get_email')
    phone = serializers.SerializerMethodField(method_name='get_phone')
    deliveryType = serializers.SerializerMethodField(method_name='get_deliveryType')
    paymentType = serializers.SerializerMethodField(method_name='get_paymentType')
    totalCost = serializers.SerializerMethodField(method_name='get_totalCost')

    # products = ProductSerializer(many=True)



    class Meta:
        model = Order
        fields = ('id',
                  'createdAt',
                  'fullName',
                  'email',
                  'phone',
                  'deliveryType',
                  'paymentType',
                  'totalCost',
                  'status',
                  'city',
                  'address',
                  'products',
                  )

    def get_createdAt(self, obj):
        return obj.created_at

    def get_fullName(self, obj):
        return obj.user.profile.fullName

    def get_email(self, obj):
        return obj.user.profile.email

    def get_phone(self, obj):
        return str(obj.user.profile.phone)

    def get_deliveryType(self, obj):
        return obj.delivery_type

    def get_paymentType(self, obj):
        return obj.payment_type

    def get_totalCost(self, obj):
        return obj.total_cost


