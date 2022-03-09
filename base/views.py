from curses.ascii import HT
from email.headerregistry import Address
from xxlimited import foo
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Customer, FavoriteFood, Food, Order, OrderFood, ShippingAddress, Menu, Category, Review
from .utils import cartCookie, guestOrder
from django.contrib import messages
from django.db.models import Q
from .forms import CreateUserForm, FoodForm, ReviewForm
import json
import datetime

# Create your views here.

def registerPage(request):
    forms = CreateUserForm()

    if request.method == 'POST':
        forms = CreateUserForm(request.POST)
        if forms.is_valid():
            user = forms.save()
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )
            return redirect('login')


    context = {'forms': forms}
    return render(request, 'base/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        print(user)

        if user is not None:
            login(request, user)
            return redirect('shop')
        else:
            messages.warning(request, 'Username or Password is incorrect!')
        

    return render(request, 'base/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

def shop(request): 

    special_foods = Food.objects.filter(menu__name='Special Dishes')
    popular_foods = Food.objects.filter(menu__name='Popular Dishes')
    today_foods = Food.objects.filter(menu__name='Today Dishes')
    reviews = Review.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartFood = order.cart_food

    else:
        data = cartCookie(request)
        items = data['items']
        order = data['order']

    context = {'special_foods': special_foods, 'popular_foods': popular_foods, 'today_foods': today_foods,
    "order": order, 'reviews': reviews}
    return render(request, 'base/food.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderfood_set.all()
        print(items)
    else:
        data = cartCookie(request)
        items = data['items']
        order = data['order']
    context = {'items': items, 'order': order}
    return render(request, 'base/cart.html', context)

def checkOut(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderfood_set.all()
        print(items)
    else:
        data = cartCookie(request)
        items = data['items']
        order = data['order']
    context = {'items': items, 'order': order}    
    return render(request, 'base/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    foodId = data["foodId"]
    action = data['action']
    print('foodId: ', foodId, 'action: ', action)

    customer = request.user.customer
    food = Food.objects.get(id=foodId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_food, created = OrderFood.objects.get_or_create(food=food, order=order)

    if action == 'add':  
        order_food.quantity += 1
    
    elif action == 'remove':
        order_food.quantity -= 1
    
    order_food.save()

    if order_food.quantity <= 0:
        order_food.delete()

    print(food)

    return JsonResponse('Item updated', safe=False)

def submitOrder(request):
    data = json.loads(request.body)
    print(data)
    transaction_id = datetime.datetime.now().timestamp()
    total = float(data['form']['total'])
    print('total:' ,total)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        
        guest = guestOrder(request, data)
        customer = guest['customer']
        order = guest['order']
    print(total)
    print(order.cart_total)

    if total == float(order.cart_total):

        ShippingAddress.objects.create(customer=customer, order=order, address=data['address']['address'], phone=data['address']['phone'])
        order.transaction_id = transaction_id
        order.complete = True
        order.save()
    return JsonResponse('Order submited', safe=False)

def search(request):

    q = request.GET.get('q') if request.GET.get('q') else ''
    print(q)
    foods = Food.objects.filter(Q(menu__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(price__icontains=q) |
                                Q(category__name__icontains=q))

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartFood = order.cart_food

    else:
        data = cartCookie(request)
        items = data['items']
        order = data['order']
    
    context = {
        'foods': foods, 'order': order
    }
    return render(request, 'base/search.html', context)

def addFav(request, pk):
    food = Food.objects.get(id=pk)
    customer = request.user.customer
    fav_foods, created = FavoriteFood.objects.get_or_create(customer=customer, food=food)
    return redirect('shop')

def favFood(request):
    customer = request.user.customer
    foods = FavoriteFood.objects.filter(customer=customer)


    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartFood = order.cart_food

    else:
        data = cartCookie(request)
        items = data['items']
        order = data['order']

    context = {
        'favfoods': foods, 'order': order,
    }
    return render(request, 'base/fav-food.html', context)


def addFood(request):
    forms = FoodForm()

    if request.method == 'POST':
        forms = FoodForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('shop')

    context = {'forms': forms}

    return render(request, 'base/add-food.html', context)

def editFood(request, pk):
    food = Food.objects.get(id=pk)
    forms = FoodForm(instance=food)

    if request.method == "POST":
        forms = FoodForm(request.POST, request.FILES, instance=food)
        if forms.is_valid():
            forms.save()
            return redirect('shop')

    context = {
        'forms': forms,
    }
    return render(request, 'base/add-food.html', context)

def delete(request, pk):
    obj = Food.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('shop')
    context = {
        'obj': obj,
    }
    return render(request, 'base/delete.html', context)

def addReview(request):
    forms = ReviewForm()
    if request.method == 'POST':
        forms = ReviewForm(request.POST)
        if forms.is_valid():
            review = forms.save(commit=False)
            review.customer = request.user.customer
            review.save()
            print(review)
            return redirect('shop')
    context = {
        'forms': forms
    }
    return render(request, 'base/add-food.html', context)

