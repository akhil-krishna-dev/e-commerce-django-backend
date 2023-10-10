let image = document.getElementById('image-tag')

let image_list = document.getElementsByClassName('img-list')


function changeImage(e){
    image.src = e.target.src

    for (let i=0; i<image_list.length; i++){
        if (image.src === image_list[i].src){
            image_list[i].classList.add('actived-image')
        }else{
            image_list[i].classList.remove('actived-image')
        }
    }

}



let wishlistBtn = document.getElementById('wishlist-btn')
let csrf_tkn = document.getElementById('csrf-token').value
let product_id = document.getElementById('prod-id').value
console.log(product_id)
wishlistBtn.addEventListener('click',function(){

    let postObj = {
        'pid':product_id
    }
    console.log(postObj)
    fetch('/wishlist/wishlist-add/',{
        method:'POST',
        credentials: 'same-origin',
        headers:{
            'Accept':'application/json',
            'X-Requested-With':'XMLHttpRequest',
            'X-CSRFToken':csrf_tkn,
        },
        body:JSON.stringify(postObj)
    })
    .then( response => {
        return response.json();
    }).then( data => {
        console.log("json res", data);
    });
    wishlistBtn.disabled = true
    wishlistBtn.innerText = "GO TO Wishlist"
});