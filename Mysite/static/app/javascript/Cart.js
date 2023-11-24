var updateBtns = document.getElementsByClassName('update-cart')

for(i=0;i<updateBtns.length;i++) {
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId',productId,'action',action)
        console.log('user: ',user)
        if (user === "AnonymousUser") {
            console.log('User not logged')
        }
        else {
            updateUserOrder(productId,action)
        }
    })
}

function updateUserOrder(productId,action) {
    console.log('user logged in , success add')
    var url = 'Update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
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