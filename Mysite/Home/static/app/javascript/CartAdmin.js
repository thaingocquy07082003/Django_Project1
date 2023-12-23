var updateBtns = document.getElementsByClassName('update-cart')

for(i=0;i<updateBtns.length;i++) {
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        var orderId = this.dataset.orderId
        console.log('productId',productId,'action',action,'orderId',orderId)
        console.log('user: ',user)
        if (user === "AnonymousUser") {
            console.log('User not logged')
        }
        else {
            updateUserOrder(productId,action,orderId)
        }
    })
}

function updateUserOrder(productId,action,orderId) {
    console.log('user logged in , success add')
    var url = 'UpdateAdmin_item/'+orderId
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action,
            'order_id': orderId
        })
    })
     .then((response) => {
        return response.json()
     })
     .then((data) => {
        console.log('data',data)
        location.reload()
     })
     .catch((error) => {
        console.error('There was a problem with the fetch operation:', error);
      });
}