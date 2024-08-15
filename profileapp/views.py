from django.shortcuts import render
from ecommerceapp.models import *
from django.contrib import messages
from ecommerceapp.utils import cartData
from profileapp.models import *
from django.http import JsonResponse
import json

# Create your views here.
def blog (request):
    # FOR FETCH THE CART DATA
    cartdata=cartData(request)
    cartitems=cartdata["cartitems"]
    # FOR TRANSFER THE DATA TO THE HTML PAGES
    customer=Customer.objects.get(user=request.user)
    context = {'cartitems':cartitems ,'customer':customer}
    return render (request,"profile/blog.html")

##########################################################################################################################################################
def about (request):
    # FOR FETCH THE CART DATA
    cartdata=cartData(request)
    cartitems=cartdata["cartitems"]
    # FOR TRANSFER THE DATA TO THE HTML PAGES
    customer=Customer.objects.get(user=request.user)
    context = {'cartitems':cartitems ,'customer':customer}
    return render (request,"profile/about.html",context)

##########################################################################################################################################################
def myprofile (request):
    # FOR FETCH THE CART DATA
    cartdata=cartData(request)
    cartitems=cartdata["cartitems"]
    # FOR TRANSFER THE DATA TO THE HTML PAGES
    customer=Customer.objects.get(user=request.user)
    if request.method=='POST':
        data=request.POST
        name=data['name']
        lastname=data['lastname']
        dob=data['dob']
        phone=data['phone']
        photo=data['photo']
        gender=data['gender']
        print(name,lastname,dob,phone,photo,gender)
        if name:
            customer.firstname=name
        if lastname:
            customer.lastname=lastname
        if dob:
            customer.dob=dob
        if phone:
            customer.mobileno=phone
        if photo:
            customer.image=photo
        if gender:
            customer.gender=gender
        customer.save()
    context = {'cartitems':cartitems ,'customer':customer}
    return render (request,"profile/profile.html",context)

##########################################################################################################################################################
def contact (request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        desc=request.POST['desc']
        phonenumber=request.POST['pnumber']
        myquery=ContactUs(name=name,email=email,desc=desc,phonenumber=phonenumber)
        myquery.save()
        messages.info(request,"WE Will Be Get Back To You")
    # FOR FETCH THE CART DATA
    cartdata=cartData(request)
    cartitems=cartdata["cartitems"]
    # FOR TRANSFER THE DATA TO THE HTML PAGES
    customer=Customer.objects.get(user=request.user)
    context = {'cartitems':cartitems ,'customer':customer}
    return render (request,"profile/contact.html",context)

##########################################################################################################################################################
def address (request):
    # FOR FETCH THE CART DATA
    cartdata=cartData(request)
    cartitems=cartdata["cartitems"]
    # FOR TRANSFER THE DATA TO THE HTML PAGES
    customer=Customer.objects.get(user=request.user)
    shippingaddress=ShippingAddress.objects.filter(customer=customer)
    customer=Customer.objects.get(user=request.user)
    context = {'cartitems':cartitems,'shippingaddress':shippingaddress,'customer':customer}
    return render (request,"profile/address.html",context)

def wishlist(request):
    data = json.loads(request.body.decode('utf-8'))
    id=int(data.get('id'))
    customer=Customer.objects.get(user=request.user)
    product=Product.objects.get(product_id=id)
    wishlistss=Wishlist.objects.filter(customer=customer)
    print("hiiiii",wishlistss)
    try:
        wishlists=Wishlist.objects.get(customer=customer,product=product)
        wishlists.delete()
    except:
        wishlishts=Wishlist.objects.create(customer=customer,product=product)
        wishlishts.save()    
    print(id)
    return JsonResponse({'message': 'Item updated successfully'}, status=200)

def wishlistHtml(request):
    products=Product.objects.all()
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        wishlists=Wishlist.objects.filter(customer=customer)
        wishlist={wish.product.product_id for wish in wishlists}
    else:
        return(request,"authentication/login.html")
    context={"products":products,"wishlist":wishlist}
    return render(request,"profile/wishlist.html",context)