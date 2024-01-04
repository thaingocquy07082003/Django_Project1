from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import slugify
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import ShippingAddress
from django.contrib.auth import login,logout,authenticate
# Create your views here.
def Search_Order(request):
    username=request.POST.get('username')
    user = User.objects.get(username=username)

    incomplete_orders = Order.objects.filter(complete=True,customer=user.customer)  # Lấy các đơn hàng đã được khách hàng hoàn thành từ database
    context = {
        'orders': incomplete_orders
    }
    return render(request, 'OrderDetail.html', context)

def introduce(request):
    return render(request, 'introduce.html')

def contact_view(request):
    return render(request, 'contact.html')

def get_chat(request):
    return render(request, 'ChatRoom.html')

def search_view(request):
    query = request.GET.get('q', '')  
    results = Product.objects.filter(name__icontains=query)  
    return render(request, 'search_results.html', {'products': results, 'query': query})

def Get_Product_Detail(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id = product_id)
    context = {'product':product}
    return render(request, 'Detail.html', context)

def Get_to_infor(request):
    customer = request.user.customer
    name = request.user.first_name + '' + request.user.last_name
    email = customer.email 
    context = {'name':name,'email':email}
    return render(request, 'Information.html', context)

def Change_infor(request):
    if request.user.is_authenticated:   
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        Customer.objects.filter(user=request.user).update(email=email)
        user_to_update = User.objects.get(username=request.user.username)
        user_to_update.set_password(password)
        user_to_update.save()
    context = {'name':name,'password':password,'email':email}
    return get_home(request)

def Get_Customer_Order(request):
    if request.user.is_authenticated:
        current_customer = request.user.customer
        # Lấy danh sách các đơn hàng của người dùng hiện tại
        orders = Order.objects.filter(customer=current_customer,complete=True)
        cost = 0.0
        total = 0.0
        items = []
        for order in orders:
            item_list = order.orderitem_set.all()
            for item in item_list:
                items.append(item)
            total+= sum([item.quantity for item in item_list])
            cost+= sum([item.get_total for item in item_list])
    else:
        orders = []
        cost = 0
        total = 0
    
    context = {'order': orders, 'cost': cost, 'total': total,'items':items}
    return render(request, 'CustomerOrder.html', context)

class ShippingAddressForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}),
    )
    state = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
    )
    moblie = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'moblie'}),
    )
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'moblie']

def get_t1(request):
    return render(request,'T1.html')

def get_t2(request):
    return render(request,'T2.html')

def get_t3(request):
    return render(request,'T3.html')

def get_manage(request):
    return render(request,'Manage.html')

# lưu ý chỗ này để xử lí các tác vụ thêm bớt các orderitem chỉ dành riêng cho admin
def UpdateItemAdmin(request, order_id):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    # orderId = data['order_id']
    # customer = request.user.customer
    product = Product.objects.get(id = productId)
    order = get_object_or_404(Order, pk=order_id)
    orderItem , created = OrderItem.objects.get_or_create(order=order,product=product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added',safe=False)

def order_item_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = order.orderitem_set.all()  # Lấy các OrderItem của đơn hàng này
    Ship = ShippingAddress.objects.get(order=order)
    context = {
        'order': order,
        'items': order_items,
        'Ship': Ship,
    }
    return render(request, 'OrderItemDetail.html', context)

def get_orderdetail(request):
    incomplete_orders = Order.objects.filter(complete=True)  # Lấy các đơn hàng đã được khách hàng hoàn thành từ database
    context = {
        'orders': incomplete_orders
    }
    return render(request, 'OrderDetail.html', context)

def logoutPage(request):
    logout(request)
    return redirect('Login')
def Register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Lưu User nhưng chưa commit vào database
            user.is_active = True
            user.save()

            # Tạo một đối tượng Customer và liên kết với user vừa tạo
            Customer.objects.create(user=user, name=user.first_name, email="thaingocquydz@gmail.com")
            latest_room = Room.objects.order_by('-id').first()
            if latest_room:
                latest_slug = int(latest_room.slug.split('-')[-1]) + 1
            else:
                latest_slug = 1
            room = Room.objects.create(name=user.username, slug=f"{latest_slug}")

            # Đăng nhập người dùng mới
            login(request, user)

            # Chuyển hướng người dùng tới trang sau khi đăng ký thành công
            return redirect('home')
        else:
            # If form is not valid, display form errors
            messages.error(request, 'Please correct the error below.')

    context = {'form': form}
    return render(request, 'Login_signup.html', context)
def get_signup(request):
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
    formShip = ShippingAddressForm(request.POST or None)
    
    if request.method == 'POST' and formShip.is_valid():
        shipping_address = formShip.save(commit=False)
        # Đặt customer từ user hiện tại
        shipping_address.customer = request.user.customer
        # Tìm order chưa hoàn thành của customer
        order = Order.objects.filter(customer=request.user.customer, complete=False).first()
        if not order:
            # Handle trường hợp không có order chưa hoàn thành
            # Có thể hiển thị thông báo hoặc tạo order mới
            pass
        else:
            shipping_address.order = order
            AllShipping = ShippingAddress.objects.filter(order=order).first()
            if AllShipping:
                ShippingAddress.objects.filter().update(order=order).update(address=shipping_address.address,city=shipping_address.city,state=shipping_address.state,moblie=shipping_address.moblie)
            else:
                shipping_address.save()
            Order.objects.filter(customer=customer, complete=False).update(complete=True)
            return redirect('home')  # redirect đến trang mong muốn sau khi lưu
    context = {'items':items,'order':order,'formShip':formShip}
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

