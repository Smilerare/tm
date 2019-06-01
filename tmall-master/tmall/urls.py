"""tmall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app.views import app, product, forecategory, addcart, cart,foredeleteOrderItem,order,saveorder,changecart,changecart1,foredeleteOrder
from app.users import login,regist,logout
from app.myadmin import myadmin, admin_category_list, admin_order_list, admin_user_list, admin_category_add, \
    admin_category_delete, admin_category_edit, admin_property_list, admin_property_add, admin_property_edit, \
    admin_property_delete, admin_product_list, admin_product_add, admin_product_delete, admin_product_edit, \
    admin_product_editPropertyValue, admin_productImage_list, admin_productImage_add, admin_productImage_delete

urlpatterns = [
    url(r'^$', app,name="index"),
    url(r'^login/', login,name="login"),
    url(r'^product/', product,name="product"),
    url(r'^forecategory/', forecategory,name="forecategory"),
    url(r'^addcart/', addcart,name="addcart"),
    url(r'^cart/', cart,name="cart"),
    url(r'^logout/', logout,name="logout"),
    url(r'^regist/', regist,name="regist"),
    url(r'^admin/', admin.site.urls),
    url(r'^myadmin/', myadmin),
    url(r'^admin_category_list/',admin_category_list,name="admin_category_list"),
    url(r'^admin_category_add/',admin_category_add,name="admin_category_add"),
    url(r'^admin_category_delete/',admin_category_delete,name="admin_category_delete"),
    url(r'^admin_category_edit/',admin_category_edit,name="admin_category_edit"),
    url(r'^admin_property_list/',admin_property_list,name="admin_property_list"),
    url(r'^admin_property_add/', admin_property_add, name="admin_property_add"),
    url(r'^admin_property_edit/', admin_property_edit, name="admin_property_edit"),
    url(r'^admin_property_delete/', admin_property_delete, name="admin_property_delete"),
    url(r'^admin_product_list/',admin_product_list,name="admin_product_list"),
    url(r'^admin_product_add/',admin_product_add,name="admin_product_add"),
    url(r'^admin_product_delete/',admin_product_delete,name="admin_product_delete"),
    url(r'^admin_product_edit/',admin_product_edit,name="admin_product_edit"),
    url(r'^admin_product_editPropertyValue/',admin_product_editPropertyValue,name="admin_product_editPropertyValue"),
    url(r'^admin_productImage_list/',admin_productImage_list,name="admin_productImage_list"),
    url(r'^admin_productImage_add/',admin_productImage_add,name="admin_productImage_add"),
    url(r'^admin_productImage_delete/',admin_productImage_delete,name="admin_productImage_delete"),
    url(r'^admin_order_list/',admin_order_list,name="admin_order_list"),
    url(r'^admin_user_list/',admin_user_list,name="admin_user_list"),

    #删除购物车商品
    url(r'^foredeleteOrderItem/',foredeleteOrderItem,name="foredeleteOrderItem"),
    #我的订单
    url(r'^order/',order,name="order"),
    #结算
    url(r'^saveorder/',saveorder,name="saveorder"),
    #改变数据库ischose为1
    url(r'^changecart/',changecart,name="changecart"),
    #改变数据库ischose为0
    url(r'^changecart1/',changecart1,name="changecart1"),
    #删除订单
    url(r'^foredeleteOrder/',foredeleteOrder,name="foredeleteOrder"),

]