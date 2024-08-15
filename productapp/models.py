from django.db import models

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=100,blank=True,null=True)
    category_image=models.ImageField(upload_to="shop/category_images", null=True,blank=True)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    sub_category_name=models.CharField(max_length=100,blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True,null=True)
    sub_category_image=models.ImageField(upload_to="shop/subcategory_images", null=True,blank=True)

    def __str__(self):
        return self.sub_category_name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL ,blank=True,null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL,blank=True,null=True)
    image1 = models.ImageField(upload_to='shop/product_images',blank=True,null=True)
    image2 = models.ImageField(upload_to='shop/product_images',blank=True,null=True)
    image3 = models.ImageField(upload_to='shop/product_images',blank=True,null=True)
    image4 = models.ImageField(upload_to='shop/product_images',blank=True,null=True)
    image5 = models.ImageField(upload_to='shop/product_images',blank=True,null=True)
    Highlights = models.TextField(blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=2, decimal_places=0, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=255, blank=True)
    material = models.CharField(max_length=255, blank=True)
    brand = models.CharField(max_length=255)
    technical_specifications = models.TextField(blank=True)
    customer_reviews = models.TextField(blank=True)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    keywords = models.CharField(max_length=1000, blank=True)
    warranty_information = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

