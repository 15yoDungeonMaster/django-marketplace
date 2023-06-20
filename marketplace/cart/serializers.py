from rest_framework import serializers

from app_shop.serializers import ProductSerializer
from cart.models import BasketProduct, Basket


class BasketProductSerializer(serializers.HyperlinkedModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = BasketProduct
        fields = ('products', )


class BasketSerializer(serializers.HyperlinkedModelSerializer):
    basket_products = BasketProductSerializer(many=True)

    class Meta:
        model = Basket
        fields = ('basket_products', )