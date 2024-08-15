from django.shortcuts import render,redirect
from ecommerceapp.models import *
from profileapp.models import *
from productapp.models import *
from ecommerceapp.utils import serchData,cartData,getAlltheOrders,filterData
import json
from django.http import JsonResponse
import datetime
import razorpay
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def store(request):
    # FOR FETCH THE CART DATA
    cartdata=cartData(request)
    cartitems=cartdata["cartitems"]
    products=Product.objects.all()
    product_dict = Product.objects.values('category','product_id')
    category = {items['category'] for items in product_dict}
    categorys=Category.objects.all()
    subcategorys=SubCategory.objects.all()

    # FOR TRANSFER THE DATA TO THE HTML PAGES
    context = {'products': products,'product_category':category,'cartitems':cartitems,'categorys':categorys,'subcategorys':subcategorys}

    return render(request, "store/store.html", context)
##########################################################################################################################################################
def searchProduct(request):
    cartdata = cartData(request)
    cartitems = cartdata["cartitems"]
    # FOR SEARCHING THE DATA
    searchdata=serchData(request)
    products=searchdata['products']
    productid=searchdata['productid']
    products=Product.objects.all()
    subcategorys=SubCategory.objects.all()
    wishlist=set()
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        wishlists=Wishlist.objects.filter(customer=customer)
        wishlist={wish.product.product_id for wish in wishlists}
        print(wishlist)

    context = {'products': products,'productid':productid,'cartitems':cartitems,'subcategorys':subcategorys,"wishlist":wishlist}
    return render(request,"store/search.html",context)

def searchcategory(request,id):
    cartdata = cartData(request)
    cartitems = cartdata["cartitems"]
    products=Product.objects.filter(category=id)
    subcategorys=SubCategory.objects.all()
    wishlist=set()
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        wishlists=Wishlist.objects.filter(customer=customer)
        wishlist={wish.product.product_id for wish in wishlists}
        print(wishlist)
    context = {'products': products,'cartitems':cartitems,'subcategorys':subcategorys,"wishlist":wishlist}
    return render(request,"store/search.html",context)

def searchsubcategory(request,id):
    cartdata = cartData(request)
    cartitems = cartdata["cartitems"]
    products=Product.objects.filter(subcategory=id)
    subcategorys=SubCategory.objects.all()
    wishlist=set()
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        wishlists=Wishlist.objects.filter(customer=customer)
        wishlist={wish.product.product_id for wish in wishlists}
        print(wishlist)
    context = {'products': products,'cartitems':cartitems,'subcategorys':subcategorys,"wishlist":wishlist}
    return render(request,"store/search.html",context)

def searchFilter(request):
    cartdata = cartData(request)
    cartitems = cartdata["cartitems"]
    subcategorys=SubCategory.objects.all()
    products=Product.objects.all()
    filterproducts=filterData(request)
    productid=filterproducts['productid']
    wishlist=set()
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        wishlists=Wishlist.objects.filter(customer=customer)
        wishlist={wish.product.product_id for wish in wishlists}
        print(wishlist)

    print(wishlist)
    context = {'products': products,'cartitems':cartitems,'subcategorys':subcategorys,'productid':productid,"wishlist":wishlist}
    return render(request,"store/search.html",context)

##########################################################################################################################################################
def view(request,id,no=1):
    cartdata = cartData(request)
    cartitems = cartdata["cartitems"]
    product=Product.objects.get(product_id=id)
    products=Product.objects.filter(category=product.category)
    if no==1:
        image=product.image1
    elif no==2:
        image=product.image2
    elif no==3:
        image=product.image3
    elif no==4:
        image=product.image4
    elif no==5:
        image=product.image5
    wishlist=set()
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        wishlists=Wishlist.objects.filter(customer=customer)
        wishlist={wish.product.product_id for wish in wishlists}

    context={'product':product,"cartitems":cartitems,'products':products,'image':image,'wishlist':wishlist}
    return render(request,"store/view.html",context)

##########################################################################################################################################################

def checkout (request):
    # FOR FETCH THE CART DATA
    cartdata=cartData(request)
    items=cartdata["items"]
    cartitems=cartdata["cartitems"]
    carttotal=cartdata['carttotal']
    # FOR TRANSFER THE DATA TO THE HTML PAGES
    form={}
    context={'items':items,'cartitems':cartitems,'carttotal':carttotal,"form":form}
    return render (request,"store/checkout.html",context)

##########################################################################################################################################################

def cart (request):
    cartdata=cartData(request)
    items=cartdata["items"]
    cartitems=cartdata["cartitems"]
    carttotal=cartdata['carttotal']

    context={'items':items,'cartitems':cartitems,'carttotal':carttotal}
    return render (request,"store/cart.html",context)

##########################################################################################################################################################

def updateItems(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        product_id = data.get('productId')
        action = data.get('action')

        if not product_id or not action:
            return JsonResponse({'error': 'Invalid data'}, status=400)
        try:
            product = Product.objects.get(product_id=product_id)
            customer,create=Customer.objects.get_or_create(user=request.user)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            order_item,created=OrderItems.objects.get_or_create(order=order,product=product)

            if action == 'add' or action=='buy':
                order_item.quantity += 1
            elif action == 'remove':
                order_item.quantity -= 1

            if order_item.quantity <= 0:
                order_item.delete()
            else:
                order_item.save()

            return JsonResponse({'message': 'Item updated successfully'}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

##########################################################################################################################################################

def processOrder(request):
    # FOR FETCH THE CART DATA
    cartdata=cartData(request)
    items=cartdata["items"]
    cartitems=cartdata["cartitems"]
    carttotal=cartdata['carttotal']
    form={}
    payment_response={}
    if request.method == 'POST':
        # CONTEXT DICTIONARY
        data = request.POST
        name=data['name']
        phone=data['phone']
        address=data['address']
        landmark=data['landmark']
        state=data['state']
        city=data['city']
        zipcode=data['zipcode']
        country=data['country']
        form={"name":name,"phone":phone,"address":address,"landmark":landmark,"state":state,"city":city,"zipcode":zipcode,"country":country}
        
    
        # PAYMENT GENERATE
        amount=int(carttotal)*100

        client=razorpay.Client(auth=('',''))
        payment_response=client.order.create({'amount':amount,"currency":"INR"})
        payment_response['name']=name
        payment_response['email']=request.user.email
        print(payment_response)

        order_id=payment_response['id']
        payment_status=payment_response['status']
        # PAYMENT VALIDATION
        if payment_status=="created":
            customer,create=Customer.objects.get_or_create(user=request.user)
            shipping=ShippingAddress(customer=customer,name=name,phone=phone,address=address,landmark=landmark,state=state,city=city,zipcode=zipcode,country=country)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            order.shipping=shipping
            order.order_id = order_id
            order.complete = True
            payment=PaymentHistory(customer=customer,price=(amount/100),order=order,order_ids=order_id)

            shipping.save()
            order.save()
            payment.save()

    context={'items':items,'cartitems':cartitems,'carttotal':carttotal,"form":form,"payment":payment_response}
    return render(request,"store/checkout.html",context)
    
    

##########################################################################################################################################################
def orderItems(request):
    cartdata = cartData(request)
    cartitems = cartdata["cartitems"]
    orders=getAlltheOrders(request)
    orderItems=orders['orderItems']
    confirm_order=orders['confirm_order']
    customer=Customer.objects.get(user=request.user)
    

    context={'cartitems':cartitems, 'confirm_orders':confirm_order,'orderItems':orderItems,'customer':customer}
    return render(request, "store/order.html", context)

@csrf_exempt
def paymentStatus(request):
    response=request.POST
    print(response)
    params_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature'],
    }
    client=razorpay.Client(auth=('',''))
    try:
        status=client.utility.verify_payment_signature(params_dict)
        payment=PaymentHistory.objects.get(order_ids=response['razorpay_order_id'])
        payment.trnasaction_id=response['razorpay_payment_id']
        payment.status=True
        payment.save()
        return render(request,"store/payment-status.html",{'status':True})
    except:
        return render(request,"store/payment-status.html",{'status':False})
        
    




