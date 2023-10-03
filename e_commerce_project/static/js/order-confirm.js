
let edit_btn = document.getElementsByClassName('address-edit-btn')

let address_container = document.getElementsByClassName('address-container')

let each_address = document.getElementsByClassName('address-display-none')




function editAddress (e){

    if (e.target.localName === 'span'){
        e.target.parentElement.nextSibling.nextElementSibling.classList.add('hide-address')
        e.target.parentElement.hidden = "true";

    }
   
}