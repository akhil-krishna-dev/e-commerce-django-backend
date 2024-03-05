
let delivery = document.getElementById('delivery-addres-websocket')
let user_id = document.getElementById('user_id').innerText

let url = `ws://${window.location.host}/ws/order-updates/${user_id}/`
let order_update = new WebSocket(url)


order_update.onopen = (e) => {
    console.log('opened connection')
}

order_update.onmessage = (e) => {
    let data = JSON.parse(e.data)
    console.log('data message ',data)
    if (data.type === 'order_update'){
        document.getElementById('status-element').innerText = data.message
    }
}

delivery.addEventListener('click',() => {
    console.log(user_id)

})


