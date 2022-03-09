from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkOut, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('checkout/', views.checkOut, name='checkout'),
    path('submit_order/', views.submitOrder, name='submit_order'),
    path('search/', views.search, name='search'),
    path('add_food/', views.addFood, name='add_food'),
    path('edit_food/<str:pk>/', views.editFood, name='edit_food'),
    path('delete_food/<str:pk>', views.delete, name='delete_food'),
    path('add_fav/<str:pk>/', views.addFav, name='add_fav'),
    path('fav_food/', views.favFood, name='fav_food'),
    path('add_review/', views.addReview, name='add_review'),





]