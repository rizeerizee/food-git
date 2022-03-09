from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Food, Review
from django.forms import ModelForm, modelform_factory

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['message']