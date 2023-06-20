from django.urls import path

from .views import CategoriesAPIView, CatalogAPIView, TagsAPIView, PopularProductsView, LimitedProductsView, \
    SaleProductsView, BannerProductsView, OrdersListAPIView, OrderRetrieveAPIView, PaymentAPIView, \
    ProductRetrieveAPIView, ReviewAPIView

urlpatterns = [
    path('categories', CategoriesAPIView.as_view(), name='categories-list'),
    path('catalog', CatalogAPIView.as_view(), name='catalog-list'),
    path('products/popular', PopularProductsView.as_view(), name='popular-products'),
    path('products/limited', LimitedProductsView.as_view(), name='limited-products'),
    path('sales', SaleProductsView.as_view(), name='sales-products'),
    path('banners', BannerProductsView.as_view(), name='banners-products'),
    path('tags', TagsAPIView.as_view(), name='tags-list'),
    path('orders', OrdersListAPIView.as_view(), name='orders-list'),
    path('order/<int:pk>', OrderRetrieveAPIView.as_view(), name='order-detail'),
    path('payment', PaymentAPIView.as_view(), name='payment-detail'),
    path('product/<int:pk>', ProductRetrieveAPIView.as_view(), name='product-detail'),
    path('product/<int:pk>/reviews', ReviewAPIView.as_view(), name='product-review')

]
