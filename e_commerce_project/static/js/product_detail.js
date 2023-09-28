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