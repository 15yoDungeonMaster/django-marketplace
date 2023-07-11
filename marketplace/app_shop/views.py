from datetime import datetime
from decimal import Decimal

from django.db.models import Avg
from rest_framework import pagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from .models import Category, Product, Tag, Order, Review
from .serializers import CategorySerializer, ProductSerializer, TagsSerializer, OrderSerializer, \
    ProductDetailSerializer, ReviewSerializer


# Create your views here.

class CategoriesAPIView(ListAPIView):
    """ Список категорий """
    queryset = Category.objects.filter(active=True, parent=None).order_by('id').prefetch_related('subcategories')
    serializer_class = CategorySerializer


class CustomCatalogPagination(pagination.PageNumberPagination):
    """
    Кастомная пагинация с помощью PageNumberPagination
    Метод get_paginated_response переопределен для соответствия с swagger
    """
    page_size = 1
    max_page_size = 100
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages
        })


class CatalogAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    pagination_class = CustomCatalogPagination

    def get_queryset(self):
        if self.request.query_params:
            filter_data = {}
            if self.request.query_params['filter[name]']:
                title = self.request.query_params['filter[name]']
                filter_data['title__contains'] = title
            if self.request.query_params['filter[minPrice]']:
                min_price = self.request.query_params['filter[minPrice]']
                filter_data['price__gte'] = float(min_price)
            if self.request.query_params['filter[maxPrice]']:
                max_price = Decimal(self.request.query_params['filter[maxPrice]'])

                filter_data['price__lte'] = float(max_price)
            if self.request.query_params['filter[freeDelivery]']:
                free_delivery = self.request.query_params['filter[freeDelivery]'].capitalize()
                filter_data['free_delivery'] = free_delivery
            if self.request.query_params['filter[available]']:
                available = self.request.query_params['filter[available]'].capitalize()
                filter_data['available'] = available
            if self.request.query_params['category']:
                category_id = self.request.query_params['category']
                category = Category.objects.get(id=category_id)
                if category.parent:
                    # print("It's subcategory")
                    filter_data['category'] = category_id
                else:
                    # print("It's category")
                    subcategories_id_list = [subcategory for subcategory in category.subcategories.values_list('id')]
                    subcategories_id_list.append(category_id)
                    filter_data['category__in'] = subcategories_id_list
            if self.request.query_params['sort']:
                sort_by = self.request.query_params['sort']
            if self.request.query_params['sortType']:
                sort_type = self.request.query_params['sortType']
                if sort_type == 'dec':
                    sort_by = '-' + sort_by
            queryset = Product.objects.prefetch_related('images').filter(**filter_data).annotate(
                rating=Avg('reviews__rate')).order_by(sort_by)
            return queryset
        return Product.objects.prefetch_related('images').all()


class PopularProductsView(ListAPIView):
    """Список из 5 продуктов с наивысшим рейтингом"""
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.prefetch_related('images').annotate(rating=Avg('reviews__rate')).order_by('-rating')[:5]


class LimitedProductsView(ListAPIView):
    """Список из 5 продуктов с самым низким количеством"""
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.prefetch_related('images').order_by('quantity')[:5]


class SaleProductsView(ListAPIView):
    """Список продуктов у которых имеется скидка, т.е значение поля discount > 0"""
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    pagination_class = CustomCatalogPagination

    def get_queryset(self):
        return Product.objects.prefetch_related('images').filter(discount__gt=0)


class BannerProductsView(ListAPIView):
    """Список из 5 последних продуктов для баннеров"""
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    pagination_class = CustomCatalogPagination

    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()[:5]


class TagsAPIView(ListAPIView):
    """Список из 5 последних тегов"""
    queryset = Tag.objects.all()[:5]
    serializer_class = TagsSerializer


class OrdersListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related('user')

    def get_cart_items(self, cart):
        cart_items = []
        for item in cart:
            product = Product.objects.get(id=item["product_id"])
            cart_items.append(
                {
                    "id": product.id,
                    "category": product.category.id,
                    "price": float(item["price"]),
                    "count": item["quantity"],
                    "date": product.date.strftime("%a %b %d %Y %H:%M:%S GMT%z (%Z)"),
                    "title": product.title,
                    "description": product.short_description(),
                    "freeDelivery": product.free_delivery,
                    "images": [
                        {"src": image.image.url, "alt": product.title}
                        for image in product.images.all()
                    ],
                    "tags": [
                        {"id": tag.id, "name": tag.name} for tag in product.tags.all()
                    ],
                    "reviews": product.reviews_count(),
                    "rating": product.average_rating(),
                }
            )
        return cart_items

    def post(self, request):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        order = Order(user=request.user, total_cost=cart.get_total_price(), products=cart_items)
        order.save()
        cart.clear()
        return Response({'orderId': order.id})


class OrderRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related('user')

    def post(self, request, pk):
        order = Order.objects.get(id=pk)

        order.delivery_type = request.data['deliveryType']
        order.payment_type = request.data['paymentType']
        order.status = request.data['status']
        order.city = request.data['city']
        order.address = request.data['address']
        order.save()

        return Response('successful operation')


class PaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        data = {
          "number": "9999999999999999",
          "name": self.request.user.profile.fullName,
          "month": datetime.datetime.now().month,
          "year": datetime.datetime.now().year,
          "code": "123"
        }

        return Response(data)


class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.prefetch_related('images').all()


class ReviewAPIView(APIView):

    def post(self, request, pk):
        print(request.data)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = Review(product=Product.objects.get(id=pk), author=self.request.user, rate=serializer.data.get('rate'), text=serializer.data.get('text'))
            review.save()
            return Response('successful operation')