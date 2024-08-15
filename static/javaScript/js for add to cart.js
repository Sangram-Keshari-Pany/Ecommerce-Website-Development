var updates=document.querySelectorAll('#update-cart')
console.log("cart.js");
if (user!='AnonymousUser'){
    cart={}
    document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/" 
}

// THIS FUNCTION IS USED TO  ADD TO CART THE PRODUCT AND INCRESE AND DECRESE THE QUANTITY
updates.forEach((element)=>{
    element.addEventListener('click',function(){
        let productId=this.dataset.product
        let action = this.dataset.action
        console.log('productid',productId,"action",action);

        console.log(user);
        if (user=='AnonymousUser'){
            console.log('not loged in'); 
            addCookieItems(productId,action)  
        }
        else{
            updateUserOrder(productId,action)

            
        }
    })
})

// THIS FUNCTION IS USED TO STORE THE CART DATA OF UNUTENTICATED USERS
function addCookieItems(productId,action){
    console.log('user not loged in ......');
    

    if (action=='add'){
        if (cart[productId]==undefined){
            cart[productId]={'quantity':1}
        }
        else{
            cart[productId]['quantity']+=1
        }

    }

    if (action=='remove'){

        console.log(cart[productId]['quantity']);
        
        cart[productId]['quantity']-=1

        if (cart[productId]['quantity']<=0){
            console.log('Remove items');
            delete cart[productId]
        }
    }

    console.log('cart :',cart);
    document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/"

    location.reload()
    
}

// THIS FUNCTION IS USED TO SEND THE DATA USING FETCH API 
// THE CART DTAA OF AUTHENTICATED USERS AND IT CHANGES THE IN VIEWS.PY
function updateUserOrder(priductId,action){
    console.log("user is login , sending data");
    var url='/updateitems'

    fetch(url,{
        method:'POST',
        headers:{
            'Content_Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify({'productId':priductId,'action':action})
    })

    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data',data);
        if (action=='add'||action=='remove')
        location.reload()
    })
    
}

