from django.urls import path, include

from cart.views import CartAPIView

urlpatterns = [

    path('basket', CartAPIView.as_view(), name='basket'),

]
