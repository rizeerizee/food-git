updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var foodId = this.dataset.food
        var action = this.dataset.action
        console.log('foodId: ', foodId, 'action: ', action)

        console.log('User: ', user)
        if (user === 'AnonymousUser'){
            cookieData(foodId, action)
        }
        else{
            updateUserFood(foodId, action)

        }
    })
}

function updateUserFood(foodId, action){

    console.log('You are authenticated, sending data...')

    url = '/update_item/'

    fetch(url, {
        method:"POST",
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'foodId': foodId, 'action': action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()

    })

}

function cookieData(foodId, action){
    console.log('Cookie data sending....')

    if (action == 'add'){
        if (cart[foodId] == undefined){
            cart[foodId] = {'quantity': 1}
        }
        else{
            cart[foodId]['quantity'] += 1
        }
    }

    if (action == 'remove'){
        cart[foodId]['quantity'] -= 1
    }

    if (cart[foodId]['quantity'] <= 0){
        console.log('Item should be deleted')
        delete cart[foodId]
    }

    console.log('Cart: ', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()

}