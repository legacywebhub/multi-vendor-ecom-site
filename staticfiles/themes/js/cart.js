updateBtns = document.getElementsByClassName('update-cart');

for (i=0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product;
        let action = this.dataset.action;
        console.log('ProductId:',productId, 'Action:', action);


        if(user == 'AnonymousUser'){
            // If user is not authenticated
            updateUserOrder(productId, action);
        } else {
            // If user is authenticated
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action){
    var url = '/update_item/'

    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:', data)
        location.reload()
    })
}