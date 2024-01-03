from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
# Create your models here.
class CustomUserCreationForm(UserCreationForm):
    # Tùy chỉnh style cho trường username
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'first name'}),
    )
    # Tùy chỉnh style cho trường password1 và password2
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Last name'}),
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'enter User name'}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Confirm your password'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Confirm your password'}),
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1','password2']

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=False)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=False)    # xet xem la laptop hay la phu kien dien tu
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)  # xet xem order nay da hoan thanh hay chua 
    transaction_id = models.CharField(max_length=200,null=True)      # Id thong tin giao dich 

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])    # so luong 
        return total
    def get_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitem])   # gia ca 
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    moblie = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
class Room(models.Model):
    # name = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)                    # tên phòng
    slug = models.SlugField(max_length=100)
    def __str__(self):
        return "Room : "+ self.name + " | Id : " + self.slug 
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return "Message is :- "+ self.content