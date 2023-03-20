let updateBtns = document.getElementsByClassName('update-cart'),
    popup = document.querySelector('#popup'),
    closePopup = popup.querySelector('#close-popup');


closePopup.addEventListener('click', ()=>{
    popup.style.display='none';
})

for (i=0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product;
        let action = this.dataset.action;
        console.log('ProductId:',productId, 'Action:', action);
        console.log(user);


        if(user == 'AnonymousUser'){
            // If user is not authenticated
            displayErrorMessage('Please sign in to create your cart', 'green', 3000);
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



function displayErrorMessage(message, bgcolor, time) {
    popup.innerHtml = `<h6>${message}</h6>`;
    popup.style.backgroundColor = bgcolor;
    popup.style.display = 'contents';
    setTimeout(()=>{
        popup.style.display = 'none';
    }, time)
}