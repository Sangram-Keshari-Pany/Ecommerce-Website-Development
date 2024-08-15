from django.urls import path
from profileapp.views import *

urlpatterns=[
    path('blog',blog,name='blog'),
    path('about',about,name='about'),
    path('myprofile',myprofile,name='myprofile'),
    path('contact',contact,name='contact'),
    path('address',address,name='address'),
    path('wishlist',wishlist,name='wishlist'),
    path('wishlist-page',wishlistHtml,name='wishlist-page')
]