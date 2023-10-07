
let edit_btn = document.getElementsByClassName('address-edit-btn')

let address_container = document.getElementsByClassName('address-container')

let each_address = document.getElementsByClassName('address-display-none')

let my_form = document.getElementById('my-form')

let address_selection_payment = document.getElementById('address-selection-payment')

function selectingAddress(e){
   console.log(e.target.value)
      adres_value = e.target.value 
      console.log(address_selection_payment) 
      address_selection_payment.setAttribute('value',adres_value)
      console.log(address_selection_payment)
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




