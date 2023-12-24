"""
URL configuration for Mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Home import views as home
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("admin/", admin.site.urls),
    path('',home.get_home,name="home"),
    path('Register/',home.Register,name="Signup"),
    path('Login/',home.get_Login,name="Login"),
    path('Logout/',home.logoutPage,name="logout"),
    path('Cart/',home.Cart,name="Cart"),
    path('Checkout/',home.Checkout,name="Checkout"),
    path('Update_item/',home.UpdateItem,name="Update_item"),
    path('Cart/Update_item/',home.UpdateItem,name="Cart_Update_item"),   # url nay chi la de xu ly them bot item trong trang Cart
    path("Rooms/", home.rooms, name="rooms"),
    path("<str:slug>", home.room, name="room"),
    path("Feedback/", home.get_orderdetail, name="orderdetail"),
    path("Manage/", home.get_manage, name="manage"),    
    path("T1/", home.get_t1, name="t1"), 
    path("T2/", home.get_t2, name="t2"), 
    path("T3/", home.get_t3, name="t3"), 
    path("Roomsadmin/", home.rooms_admin, name="roomsadmin"),
    path('order/<int:order_id>/', home.order_item_detail, name='order_item_detail'),
    path('order/<int:order_id>/UpdateAdmin_item/', home.UpdateItemAdmin, name='admin_update_item'),   # cái này là đường dẫn cho việc update từng orderitem dành riêng cho admin
    path('UpdateAdmin_item/',home.UpdateItemAdmin,name="UpdateAdmin_item"),
    path('CustomerOrder/',home.Get_Customer_Order,name="customerOrder"),
    path('GetToInfor/',home.Get_to_infor,name="gettoinfor"),
    path('ChangeInfor/',home.Change_infor,name="change_infor"),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
