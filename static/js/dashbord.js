let account_detail = document.getElementsByClassName('account-details section')[0]
let dashbord_order_address = document.getElementsByClassName('dashboard-order-address section')[0]
let wishlist_container = document.getElementsByClassName('all-wishlist-products')[0]

let wishlistBtn = document.getElementsByClassName('profile-wishlist menu')[0]
let profileBtn = document.getElementsByClassName('profile-details')[0]


wishlistBtn.addEventListener('click',function(){
    account_detail.style.display = "none"
    dashbord_order_address.style.display = "none"
    wishlist_container.style.display = "block"

    wishlistBtn.classList.add("active");
    profileBtn.classList.remove("active");
})

profileBtn.addEventListener('click',function(){
    account_detail.style.display = "block"
    dashbord_order_address.style.display = "block"
    wishlist_container.style.display = "none"

    wishlistBtn.classList.remove("active");
    profileBtn.classList.add("active");
})



// profile pic form hide and show

let form = document.getElementsByClassName('profile-upload')[0]
let hide_btn = document.getElementsByClassName('form-hide-btn')[0]

hide_btn.addEventListener('click',function(){
    console.log(form.hidden)
    if (form.hidden === false){
        form.hidden =true
        hide_btn.value = "change picture"
    }else{
        form.hidden =false
        hide_btn.value = "cancel"
    }
})






