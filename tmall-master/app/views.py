from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import  render_to_response
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import random,time
from app.models import Category, Product, Productimage, Propertyvalue, Property, User, Cart,Order
def app(request):
    name = request.COOKIES.get('name', '')
    categorylist = Category.objects.all()[:4]
    clist=[]
    for i in categorylist:
        cid=i.id
        products=Product.objects.filter(cid_id=cid)#种类id和产品id对应
        ps=[]
        for j in products:
            pid=j.id
            try:
                l=Productimage.objects.filter(typ='type_single',pid_id=pid)
                id=l.first().id
                img="/static/img/productSingle/%s.jpg"%id
            except:
                img='/static/img/site/tmallbuy.png'
            product={'id':j.id,'name':j.name,'price':j.promotePrice,'img':img}
            ps.append(product)
        category={'id':i.id,'name':i.name,'products':ps}
        clist.append(category)
    return render_to_response('index.html' ,{'name':name,'clist':clist})
def product(request):
    name = request.COOKIES.get('name', '')
    pid=request.GET['pid']
    product=Product.objects.get(id=pid)
    cid=product.cid_id
    headimg="/static/img/category/%s.jpg"%cid
    images=Productimage.objects.filter(pid_id=pid,typ='type_single')
    image=[]
    for i in images:
        id=i.id
        img="/static/img/productSingle/%s.jpg"%id
        image.append(img)
    detailImages=Productimage.objects.filter(pid_id=pid,typ='type_detail')
    detailImage = []
    for i in detailImages:
        id = i.id
        img = "/static/img/productDetail/%s.jpg" % id
        detailImage.append(img)
    propertys=Property.objects.filter(cid_id=cid)
    propertyValues=[]
    for i in propertys:
        ptid=i.id
        try:
            value=Propertyvalue.objects.get(pid_id=ptid,ptid_id=pid).value
        except:
            value=''
        propertyvalue={'property':i.name,'value':value}
        propertyValues.append(propertyvalue)
    return render_to_response('product.html', {'name': name,'product':product,'headimg':headimg,'image':image,'defaultimg':image[0],'detailImage':detailImage,
                                               'propertyValues': propertyValues})
def forecategory(request):
    name = request.COOKIES.get('name', '')
    cid=request.GET['cid']
    headimg="/static/img/category/%s.jpg"%cid
    productlist = Product.objects.filter(cid_id=cid)
    products=[]
    for i in productlist:
        pid=i.id
        imgs = Productimage.objects.filter(pid_id=pid, typ='type_single')
        imgid=imgs.first().id
        img="/static/img/productSingle/%s.jpg"%imgid
        product={'id':i.id,'promotePrice':i.promotePrice,'name':i.name,'img':img}
        products.append(product)
    return render_to_response('forecategory.html', {'name': name,'headimg':headimg,'products':products})
@csrf_exempt
def addcart(request):
    if request.method == 'POST':
        pid=request.POST['pid']
        price=request.POST['add_price']
        amount=request.POST['amount']
        name=request.COOKIES.get('name', '')
        if name !='':
            uid=User.objects.get(name=name).id
            carts = Cart.objects.filter(uid=uid)
            c =None
            if carts.count() == 0:
                #直接增加一条订单
                Cart.objects.create(uid=uid,pid=pid,price=price,amount=amount)
            else:
                try:
                    c = carts.get(pid = pid)
                    #修改价格和数量
                    if c.isdelete==1:
                        c.amount = 1
                        c.price = price
                        c.isdelete = 0
                    else:
                        c.amount += 1
                        c.price = (float(price)*c.amount)
                    c.save()
                except Cart.DoesNotExist as e:
                    Cart.objects.create(uid=uid,pid=pid,price=price,amount=amount)
            return JsonResponse({"status": 'ok'})
        else:
            return JsonResponse({"status": 'no'})
@csrf_exempt
def cart(request):
    if request.method == 'GET':
        try:
            name = request.COOKIES.get('name', '')
            uid = User.objects.get(name=name).id
            cartlist=Cart.objects.filter(uid=uid,isdelete=0)
            carts=[]
            for cart in cartlist:
                price=cart.price
                amount=cart.amount
                pro=Product.objects.get(id=cart.pid)
                product = {'id':pro.id,'subTitle':pro.subTitle,'orignalPrice':pro.orignalPrice,
                         'promotePrice':pro.promotePrice,'stock':pro.stock}
                img = Productimage.objects.filter(typ="type_single", pid_id=cart.pid)
                id = img.first().id
                product['img'] = '/static/img/productSingle/%s.jpg' % id
                c={'id':cart.id,'price':price,'amount':amount,'product':product}
                carts.append(c)
            return render_to_response('cart.html', {'carts':carts,'name':name})
        except:
            return  HttpResponseRedirect('/login/')


@csrf_exempt
def foredeleteOrderItem(request):
    pid=request.POST.get('oiid')
    if pid :
        Cart.objects.filter(id=pid).delete()
        return JsonResponse({"status": 'success'})
    # else:
    #     return JsonResponse({"status": 'no'})

def order(request):
    try:
        name = request.COOKIES.get('name', '')
        uid = User.objects.get(name=name).id
    except:
        return  HttpResponseRedirect('/login/')

    Orderlist = Order.objects.all()
    if len(Orderlist) == 0:
      return render_to_response('order.html')
    Orderlist = Order.objects.filter(uid_id=uid)
    orders=[]
    for order in Orderlist:
        orderCode=order.orderCode
        createDate=order.createDate
        cartid = order.cartid
        cart = Cart.objects.filter(id = cartid)[0]
        price=cart.price
        amount=cart.amount
        pro=Product.objects.get(id=cart.pid)
        product = {'id':pro.id,'name':pro.name,'orignalPrice':pro.orignalPrice,
                 'promotePrice':pro.promotePrice,'stock':pro.stock}
        img = Productimage.objects.filter(typ="type_single", pid_id=cart.pid)
        id = img.first().id
        product['img'] = '/static/img/productSingle/%s.jpg' % id
        c={'id':order.id,'price':price,'amount':amount,'product':product,'orderCode':orderCode,'createDate':createDate}
        orders.append(c)
        #获取完所有信息删除购物车所选商品
        Cart.objects.filter(id = cartid).update(isdelete=1)
    return render_to_response('order.html', {'orders':orders,'name':name})


@csrf_exempt
def saveorder(request):
    #订单表加入所选商品
    name = request.COOKIES.get('name', '')
    uid = User.objects.get(name=name).id
    carts = Cart.objects.filter(isChose=1,isdelete=0)
    for i in range(len(carts)):
        #创建订单
        orderCode = str(random.randint(10000000000000000000,99999999999999999999))
        address = '安徽省黄山市'
        mobile = str(random.randint(10000000000,19999999999))
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        status = '待发货'
        cartid = carts[i].id
        Order.objects.create(orderCode=orderCode,address=address,post=address,receiver=name,mobile=mobile,userMessage=address,createDate=date,payDate=date,deliveryDate=date,confirmDate=date,status=status,uid_id=uid,cartid=cartid)
    return JsonResponse({"status": 'success'})

@csrf_exempt
def changecart(request):
    cid = request.POST.get('cid')
    Cart.objects.filter(id = cid).update(isChose=1)
    return JsonResponse({"status": 'success'})
@csrf_exempt
def changecart1(request):
    cid = request.POST.get('cid')
    Cart.objects.filter(id = cid).update(isChose=0)
    return JsonResponse({"status": 'success'})
#删除订单
@csrf_exempt
def foredeleteOrder(request):
    oid=request.POST.get('oid')
    if oid :
        Order.objects.filter(id=oid).delete()
    return JsonResponse({"status": 'success'})