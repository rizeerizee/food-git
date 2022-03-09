from argparse import ONE_OR_MORE
from concurrent.futures.process import _python_exit
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    avater = models.ImageField(default='pic-1.png', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            name = self.name
        except:
            name = ''
        return str(name)

    @property
    def avaterUrl(self):
        try:
            url = self.avater.url
        except:
            url = ''
        return url


class Menu(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Food(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    images = models.ImageField(default='about-img.png', null=True, blank=True)
    discount = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.images.url
        except:
            url = ''
        return url

class FavoriteFood(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def cart_food(self):
        items = self.orderfood_set.all()
        total = sum([item.quantity for item in items])
        return total

    @property
    def cart_total(self):
        items = self.orderfood_set.all()
        total = sum([item.get_total for item in items])
        return total

class OrderFood(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = (self.food.price * self.quantity)
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Review(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:20]
