from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
# Create your views here.
def get_t1(request):
    return render(request,'T1.html')

def get_t2(request):
    return render(request,'T2.html')

def get_t3(request):
    return render(request,'T3.html')

def get_manage(request):
    return render(request,'Manage.html')

def get_orderdetail(request):
    return render(request,'OrderDetail.html')

def logoutPage(request):
    logout(request)
    return redirect('Login')
def Register(request):
    # form = CustomUserCreationForm()
    # if request.method == "POST":
    #     form = CustomUserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
            
    # context ={'form':form}
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
        else:
            # If form is not valid, display form errors
            messages.error(request, 'Please correct the error below.')

    context = {'form':form}
    return render(request,'Register.html',context)
def get_signup(request):
    # if request.method == 'POST':
    #     first_name = request.POST.get('firstname','')
    #     last_name = request.POST.get('lastname','')
    #     username = request.POST.get('username','')
    #     password = request.POST.get('password','')
    #     initial_data = {'username': username,'first_name': first_name ,'last_name': last_name, 'password':password }
    #     form = UserCreationForm(initial=initial_data)
    #     if form.is_valid():
    #         form.save()
    # else:
    #     form = UserCreationForm()
    # context = {'form':form}


    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)  # Dùng dữ liệu POST trực tiếp
    #     if form.is_valid():
    #        user = form.save(commit=False)  # Tạo đối tượng người dùng nhưng chưa lưu vào CSDL
    #        user.first_name = request.POST['firstname']  # Thêm first_name cho user
    #        user.last_name = request.POST['lastname']  # Thêm last_name cho user
    #        user.save()  # Lưu người dùng vào CSDL
    #        # Đăng nhập người dùng hoặc gửi thông báo thành công tại đây nếu cần
    # else:
    #     form = UserCreationForm()
    # context = {'form':form}
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request,'Login_signup.html',context)
def get_home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , create = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products' : products , 'cartItems': cartItems}
    return render(request,'Home.html',context) 
def get_Login(request):
    if request.user.is_authenticated:
        if request.user.username == 'admin':
            return redirect('manage')
        else:
            return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.username == 'admin':
                return redirect('manage')
            else:
                return redirect('home')
        else: messages.info(request,'user or password is incorrect!')
    content = {}
    return render(request,'Login_signup.html',content)
def Cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , create = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
    context = {'items':items,'order':order}
    return render(request,'Cart.html',context)
def Checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , create = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
    context = {'items':items,'order':order}
    return render(request,'Checkout.html',context)

def UpdateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order , created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem , created = OrderItem.objects.get_or_create(order=order,product=product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added',safe=False)

def rooms(request):
    rooms=Room.objects.all()
    return render(request, "rooms.html",{"rooms":rooms})

def room(request,slug):
    room_name=Room.objects.get(slug=slug).name
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))
    return render(request, "room.html",{"room_name":room_name,"slug":slug,'messages':messages})

def rooms_admin(request):
    rooms=Room.objects.all()
    return render(request, "roomsadmin.html",{"rooms":rooms})

