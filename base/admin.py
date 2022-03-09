from typing import OrderedDict
from unicodedata import category
from django.contrib import admin
from .models import Customer, Food, Order, OrderFood, Review, ShippingAddress, Menu, Category, FavoriteFood

# Register your models here.

admin.site.register(Customer)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderFood)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(ShippingAddress)
admin.site.register(Review)
admin.site.register(FavoriteFood)