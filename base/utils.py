from .models import *
import json

def cartCookie(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
            cart = {}
    print('cart :',cart)
    items = []
    order = {'cart_food': 0, 'cart_total': 0,}
    cartItems = order['cart_food']

    for i in cart:
        try:
            if cart[i]['quantity'] > 0:
                cartItems += cart[i]['quantity']
                food = Food.objects.get(id=i)
                total = (cart[i]['quantity'] * food.price)

                order['cart_food'] += cart[i]['quantity']
                order['cart_total'] += total

                item = {
                        'id': food.id,
                        'food': {'id':food.id, 'name':food.name, 'price':food.price, 
                        'imageUrl': food.imageUrl}, 'quantity':cart[i]['quantity'],
                        'get_total': total,
                    }

                items.append(item)

        except:
            pass
    return  {'items': items, 'order': order}

def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    cart_data = cartCookie(request)

    items = cart_data['items']

    for item in items:
        food = Food.objects.get(id=item['food']['id'])
        order_food = OrderFood.objects.create(food=food, order=order, quantity=item['quantity'])

    return {'customer': customer, 'order': order}