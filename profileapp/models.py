from django.db import models
from django.contrib.auth.models import User
from productapp.models import Product
# Create your models here.
class Customer(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, null=True, blank=True) 
    lastname = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='userimages/', blank=True, null=True)
    dob = models.DateField(null=True, blank=True)  
    mobileno = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)


    def __str__(self):
        return str(self.user) if self.user else "No User"

class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)

    class Meta:
        unique_together = ('customer', 'product')

    def __str__(self):
        return str(self.customer.user.username)
    

    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    landmark = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.address}, {self.city}, {self.state}, {self.zipcode}, {self.country}"


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    desc = models.TextField(max_length=1000)
    phonenumber = models.CharField(max_length=15,null=True,blank=True)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.subject}"


