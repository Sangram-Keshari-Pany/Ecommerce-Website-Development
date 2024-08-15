console.log("wishlist.js");
let whislists=document.querySelectorAll(".wishlist")
console.log(whislists);

whislists.forEach(element => {
    element.addEventListener("click",()=>{
        if(user!='AnonymousUser'){
            wishlist(element.id)
            
        }
    })
});

function wishlist(id){
    var url="/profile/wishlist"
    fetch(url,{
        method:'POST',
        headers:{
            'Content_Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify({'id':id})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data',data);
        location.reload()
    })
}

orderbutton=document.querySelectorAll(".user-info-button")
console.log(orderbutton);
orderbutton.forEach((element)=>{
    element.addEventListener("click",()=>{
        element.style.backgroundColor="gold"
        element.style.color="black"
        element.style.border="2px solid black"
    })
})

editbutton=document.querySelector(".edit-button")
userinfoform=document.querySelector(".user-info-form")
console.log(editbutton);
console.log(userinfoform);

editbutton.addEventListener("click",()=>{
    userinfoform.style.display="block"

})
