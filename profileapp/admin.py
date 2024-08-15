from django.contrib import admin
# Register your models here.
from profileapp.models import *
admin.site.register(Customer)
admin.site.register(ShippingAddress)
admin.site.register(ContactUs)
admin.site.register(Wishlist)



