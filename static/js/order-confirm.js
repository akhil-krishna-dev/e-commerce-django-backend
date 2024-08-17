
let edit_btn = document.getElementsByClassName('address-edit-btn')

let new_address = document.getElementById('new-address-create')

let address_container = document.getElementsByClassName('address-container')

let each_address = document.getElementsByClassName('address-display-none')

let my_form = document.getElementById('my-form')

let address_selection_payment = document.getElementById('address-selection-payment')

let address_selection_cash_deli = document.getElementById('address-selection-cashdelivery')

let cash_del_btn = document.getElementsByClassName('cash-on-devilery-btn')[0]
let razorpay_btn = document.getElementsByClassName('razorpay-payment-button')[0]
let razorpay_btn_fake = document.getElementsByClassName('razorpay-payment-button-fake')[0]
let payment_opt = document.getElementsByClassName('payment-option')[0]

function selectingAddress(e){
   console.log(e.target.value)
      adres_value = e.target.value
      address_selection_payment.setAttribute('value',adres_value)
      address_selection_cash_deli.setAttribute('value',adres_value)
      cash_del_btn.disabled = false;
      razorpay_btn.disabled = false;
      razorpay_btn.value = "RazorPay";
      cash_del_btn.innerText = "Cash On Delivery";
      razorpay_btn_fake.hidden = true
      razorpay_btn.hidden = false
      cash_del_btn.hidden = false
      payment_opt.style.background = '#0d6efd'

}

if (address_selection_cash_deli.value == "val" ){
   console.log(address_selection_cash_deli.value) 
   cash_del_btn.setAttribute('disabled',true)
   razorpay_btn.setAttribute('disabled',true)
   razorpay_btn.hidden = true
   razorpay_btn_fake.addEventListener('mouseover',()=>{
      razorpay_btn_fake.innerText = 'Please select any address'
   })
   razorpay_btn_fake.addEventListener('mouseout',()=>{
      razorpay_btn_fake.innerText = 'RazorPay'  
   })
}



let address_form = document.getElementById('delivery-address-container')
let hidden_create_address = document.getElementsByClassName('hidden-create-address')[0]
let pin_address = document.getElementById('address-pincode')
let mobile = document.getElementById('address-mobile')

function editAddress (e){

    if (e.target.localName === 'span'){
        e.target.parentElement.nextSibling.nextElementSibling.classList.add('hide-address')
        e.target.parentElement.hidden = "true";

    }
   
}

function hideAddress (){
    address_form.style.display = 'none'
    my_form.style.display = 'none'
    hidden_create_address.style.display = 'block'

}
document.getElementById('create-form-back').addEventListener('click', function(){
   hidden_create_address.style.display = 'none'
   address_form.style.display = 'block'
   my_form.style.display = 'block'
})




pin_address.onchange = function(){
    console.log(pin_address.value)
    let pin = parseInt(pin_address.value);
    let mob = parseInt(mobile.value);
     if (pin_address.value = isNaN(pin)){
        console.log('not a number')
        pin_address.value = ''
     }else{
        pin_address.value = pin
     }
     
     if(mobile.value = isNaN(mob)){
        console.log('not mobile',mobile)
        mobile.value = ''
     }else{
        mobile.value=mob
     }
}


// new address submit button disable

function formSubmition(){
   new_address.innerText = "adding address"
   new_address.disabled = true
   return true
}

function cashDeliverySave(){
   cash_del_btn.disabled = true
   return true
}


