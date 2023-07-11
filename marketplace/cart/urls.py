from django.urls import path

from cart.views import CartAPIView

urlpatterns = [

    path('basket', CartAPIView.as_view(), name='basket'),

]
