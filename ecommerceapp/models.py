from django.db import models
from productapp.models import Product
from profileapp.models import Customer,ShippingAddress

# Create your models here.

##########################################################################################################################################################
# ORDER TABLE
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    shipping = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    order_id = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')
    
    def __str__(self):
        return str(self.customer) 
    
    # TO GET THE CART TOTAL PRICE
    @property
    def get_cart_total(self):
        order_items = self.order_items.all()
        total = sum([item.get_total for item in order_items])
        return total
    
    # TO GET THE TOTAL ITEM PRESENT IN THE CART
    @property
    def get_cart_items(self):
        order_items = self.order_items.all()
        cart_items = sum([item.quantity for item in order_items])
        return cart_items


##########################################################################################################################################################
# ORDER ITEMS TABLE
class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_items')
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name 
    
    @property
    def get_total(self):
        price = self.product.price
        return (price * self.quantity)

class PaymentHistory(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    price=models.BigIntegerField()
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    order_ids=models.CharField(max_length=100,blank=True,null=True)
    trnasaction_id=models.CharField(max_length=100,blank=True,null=True)
    status=models.BooleanField(default=False)
    paymentdate=models.DateField(auto_now_add=True)


