from django.contrib import admin
from ecommerceapp.models import Order,OrderItems,PaymentHistory
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(PaymentHistory)


