from django.urls import path
from ecommerceapp.views import *

urlpatterns=[
    path('',store,name='store'),
    path('search',searchProduct,name="search"),
    path('searchcategory/<int:id>',searchcategory,name="searchcategory"),
    path('searchsubcategory/<int:id>',searchsubcategory,name="searchsubcategory"),
    path("filter",searchFilter,name='filter'),
    path('view/<int:id>',view,name='view'),
    path('view/<int:id>/<int:no>',view,name='view'),
    path('checkout',checkout,name='checkout'),
    path('cart',cart,name='cart'),
    path('updateitems',updateItems,name="updateitems"),
    path('order',orderItems,name='order'),
    path('processorder',processOrder,name='processorder'),
    path('payment-status',paymentStatus,name='payment-status')
]