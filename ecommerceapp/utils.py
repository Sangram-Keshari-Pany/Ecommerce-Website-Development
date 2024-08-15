# for searching the items hear is the logic
from ecommerceapp.models import *
from productapp.models import Product
import re
import json
##########################################################################################################################################################
# FOR SEARCHING THE DATA
def serchData(request):
    products=Product.objects.all()
    # searching product
    if request.method == "POST":
        search = request.POST.get('search', '').lower()
        if search:
            category=set()
            productid=set()
            for product in products:
                searchname=re.findall(search, product.name.lower())
                if searchname:
                    productid.add(product.product_id)
            if not productid:
                for product in products:
                    searchkeyword=re.findall(search, product.keywords.lower())
                    if searchkeyword:
                        productid.add(product.product_id)
                    
    return {'products':products,'productid':productid}

##########################################################################################################################################################
# FOR ORDER AND CART DETAILS
def cartData(request):
    if request.user.is_authenticated:
        cookieCartLogin(request)
        customer,create=Customer.objects.get_or_create(user=request.user)
        order,create=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.order_items.all().order_by('product_id')
        cartItems=order.get_cart_items
        carttotal=order.get_cart_total
    else:
        cookiedata=getCookiesData(request)
        items=cookiedata['items']
        cartItems=cookiedata['cartitems']
        carttotal=cookiedata['carttotal']
       
 
    return {'items':items,'cartitems':cartItems,'carttotal':carttotal}

##########################################################################################################################################################
# TO GET THE DATA FROM COOKIES 
def getCookiesData(request):
    items=[]
    cartItems=0
    carttotal=0
    try:
        cart=json.loads(request.COOKIES['cart'])
    except:
        cart={}
    for id in cart:
        cartItems +=cart[id]['quantity']
        product=Product.objects.get(product_id=id)
        total=(product.price)*cart[id]['quantity']

        carttotal+=total

        item={
            "product":{
                'product_id':id,
                "product_name":product.name,
                "category":product.category,
                "subcategory":product.subcategory,
                "price":product.price,
                "desc":product.description,
                "image1":product.image1,
            },
            "quantity":cart[id]['quantity'],
            'get_total':total
        }
        items.append(item)
    return {'items':items,'cartitems':cartItems,'carttotal':carttotal}

##########################################################################################################################################################
# ADDING COOKIES VALUE AFTER LOGIN THE PAGE
def cookieCartLogin(request):
    print("cokieee cart")
    try:
        cart=json.loads(request.COOKIES['cart'])
        print(cart)
    except:
        cart={}
    else:
        print(cart)
        customer,create=Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        for id in cart:
            cookiequantity=cart[id]['quantity']
            product=Product.objects.get(product_id=id)
            orderItem,created=OrderItems.objects.get_or_create(order=order,product=product)
            orderItem.quantity=orderItem.quantity+cookiequantity
            orderItem.save()

##########################################################################################################################################################
# FILTERING THE ORDERS HEAR 
def getAlltheOrders(request):
    try:
        if request.user.is_authenticated:
            customer=Customer.objects.get(user=request.user)
            orders=Order.objects.filter(customer=customer)
            orderItems=OrderItems.objects.all()
            confirm_order={order.id for order in orders if order.complete}
    except:
        orderItems={}
        confirm_order=set()
    return {'confirm_order':confirm_order,'orderItems':orderItems}

##########################################################################################################################################################
# FILTERING THE DATA
def filterData(request):
    products=Product.objects.all()
    prductid={product.product_id for product in products}
    print(prductid)
    if request.method=='POST':
        category=request.POST.get('category')
        minvalue=int(request.POST.get('minvalue'))
        maxvalue=int(request.POST.get('maxvalue'))
        brand=request.POST.get('brand')            
        rating=float(request.POST.get('rating'))
        discount=float(request.POST.get('discount'))
        color=request.POST.get('color')

        categoryid={product.product_id for product in products if product.subcategory.sub_category_name==category}
        minvalueid={product.product_id for product in products if product.price>=minvalue if minvalue!=0}
        maxvalueid={product.product_id for product in products if product.price<maxvalue if maxvalue!=0}
        brandid={product.product_id for product in products if product.brand==brand}
        ratingid={product.product_id for product in products if product.average_rating>=rating if rating!=0}
        discountid={product.product_id for product in products if product.discount>=discount if discount !=0}
        colorid={product.product_id for product in products if product.color==color}

        filtering=[categoryid,minvalueid,maxvalueid,brandid,ratingid,discountid,colorid]
        filtered=[filterr for filterr in filtering if filterr]
        print(filtered)

        ids=set()
        for id in prductid:
            rotation=0
            for sets in filtered:
                if id in sets:
                    rotation+=1
            if rotation==len(filtered) and len(filtered)!=0:
                ids.add(id)
                print(ids)
        if ids:
            prductid=ids
        else:
            prductid={"invalid"}
        print("new",prductid)

        # print(category,categoryid)
        # print(maxvalue,maxvalueid)
        # print(minvalue,minvalueid)
        # print(brand,brandid)
        # print(rating,ratingid)
        # print(discount,discountid)
        # print(color,colorid)

    return {'productid':prductid}





    
