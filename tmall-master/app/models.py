from datetime import timezone

from django.db import models

# Create your models here.
#用户表
class User(models.Model):
    name= models.CharField(max_length=100)
    passwd= models.CharField(max_length=100)
    email=models.EmailField()
    isadmin=models.IntegerField(default=0)
    def __str__(self):
        return self.name
#分类表
class Category(models.Model):
    name = models.CharField(max_length=255)
#属性表
class Property(models.Model):
    cid = models.IntegerField()
    name=models.CharField(max_length=255)
    cid = models.ForeignKey(Category, on_delete=models.CASCADE)
#产品表
class Product(models.Model):
    name=models.CharField(max_length=255)#商品介绍
    subTitle = models.CharField(max_length=255)
    orignalPrice=models.FloatField()#原价
    promotePrice=models.FloatField()#商品显示价格
    stock=models.IntegerField()#库存
    cid = models.IntegerField()
    createDate = models.DateField()#创建日期
    cid = models.ForeignKey(Category, on_delete=models.CASCADE)
#属性值表
class Propertyvalue(models.Model):
    pid = models.IntegerField()
    ptid = models.IntegerField()
    value=models.CharField(max_length=255)
    pid = models.ForeignKey(Property, on_delete=models.CASCADE)
    ptid = models.ForeignKey(Product, on_delete=models.CASCADE)
#产品图片表
class Productimage(models.Model):
    pid = models.IntegerField()
    typ=models.CharField(max_length=255)
    pid = models.ForeignKey(Property, on_delete=models.CASCADE)
#评价表
class Review(models.Model):
    content = models.CharField(max_length=4000)
    uid = models.IntegerField()
    pid = models.IntegerField()
    createDate = models.DateField()
    pid = models.ForeignKey(Property, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
#订单表
class Order(models.Model):
    orderCode=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    post=models.CharField(max_length=255)
    receiver=models.CharField(max_length=255)
    mobile=models.CharField(max_length=255)
    userMessage=models.CharField(max_length=255)
    createDate= models.DateField()
    payDate= models.DateField()
    deliveryDate= models.DateField()
    confirmDate= models.DateField()
    uid=models.IntegerField()
    status=models.CharField(max_length=255)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    cartid = models.IntegerField()
    # def __str__(self):
    #     return self.order_code
#订单项表
class Orderitem(models.Model):
    pid = models.IntegerField()
    oid = models.IntegerField()
    uid = models.IntegerField()
    number=models.IntegerField()
    pid = models.ForeignKey(Property, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    oid = models.ForeignKey(Order, on_delete=models.CASCADE)
#购物车
class Cart(models.Model):
    uid=models.IntegerField()
    pid = models.IntegerField()
    price = models.FloatField()
    amount = models.IntegerField()
    isChose = models.BooleanField(default=False)
    isdelete = models.BooleanField(default=False)



