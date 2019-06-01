import os
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from app.models import User, Category, Property, Product, Propertyvalue, Productimage, Order


def md5(str):
    import hashlib
    str=str.encode("utf-8")
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()
def isadmin(request):
    if request.method =='GET':
        try:
            name = request.COOKIES.get('name', '')
            user = User.objects.get(name=name)
        except:
            return False
        if user.isadmin == 1:
            return True
        else:
            return False
def save(file,path,filename):
    destination = open(os.path.join(path, filename), 'wb+')
    for chunk in file.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
def myadmin(request):
    if request.method =='GET':
        return render(request, "adminlogin.html")
    if request.method == 'POST':
        name=request.POST['username']
        passwd=request.POST['password']
        passwd=md5(passwd)
        try:
            user=User.objects.get(name=name)
        except:
            return render(request, 'adminlogin.html',{'script':"alert",'wrong':'用户不存在'})
        if passwd==user.passwd:
            if user.isadmin==1:
                response = HttpResponseRedirect('/admin_category_list/')
                response.set_cookie('name', name, 3600)
                return response
            else:
                return render(request, 'adminlogin.html', {'script': "alert", 'wrong': '你不是管理员'})
        else:
            return render(request, 'adminlogin.html',{'script':"alert",'wrong':'密码错误'})
def admin_category_list(request):
    if request.method =='GET':
        if isadmin(request):
            Categorylist=Category.objects.all()
            clist=[]
            for i in Categorylist:
                category={'id':i.id,'name':i.name,'img':'/static/img/category/%s.jpg'%i.id}
                clist.append(category)
            return render(request, "admin_category_list.html",{'clist': clist})
        else:
            return render(request, "adminlogin.html")
def admin_category_add(request):
    if request.method=='POST':
        name=request.POST['name']
        file=request.FILES.get('file')
        if not file:
            return HttpResponse("no files for upload!")
        try:
            category = Category.objects.get(name=name)
            return render(request, 'admin_category_list.html', {'script': "alert", 'wrong': '分类已存在'})
        except:
            Category.objects.create(name=name)
            category = Category.objects.get(name=name)
            id=category.id
            filename='%s.jpg'%id
            path="./app/static/img/category/"
            save(file,path,filename)
            response = HttpResponseRedirect('/admin_category_list/')
            return response
def admin_category_delete(request):
    if request.method=='GET':
        if isadmin(request):
            id=request.GET['id']
            category=Category.objects.get(id=id)
            category.delete()
            file = "./app/static/img/category/%s.jpg" % id
            if os.path.exists(file):
                os.remove(file)
            else:
                return HttpResponse("no files")
            response = HttpResponseRedirect('/admin_category_list/')
            return response
        else:
            return render(request, "adminlogin.html")
def admin_category_edit(request):
    if request.method=='GET':
        if isadmin(request):
            id = request.GET['id']
            category = Category.objects.get(id=id)
            return render(request, "admin_category_edit.html",{'category':category})
        else:
            return render(request, "adminlogin.html")
    if request.method == 'POST':
        id = request.POST['id']
        name=request.POST['name']
        file = request.FILES.get('file')
        if not file:
            return HttpResponse("no files for upload!")
        category = Category.objects.get(id=id)
        filename = '%s.jpg' % id
        path = "./app/static/img/category/"
        save(file, path, filename)
        category.name=name
        category.save()
        response = HttpResponseRedirect('/admin_category_list/')
        return response
def admin_property_list(request):
    if request.method =='GET':
        if isadmin(request):
            cid = request.GET['cid']
            propertylist=Property.objects.filter(cid_id=cid)
            return render(request, "admin_property_list.html",{"plist":propertylist,"cid":cid})
        else:
            return render(request, "adminlogin.html")
def admin_property_add(request):
    if request.method=='POST':
        name=request.POST['name']
        cid=request.POST['cid']
        Property.objects.create(name=name,cid_id=cid)
        response = HttpResponseRedirect('/admin_property_list/?cid=%s'%cid)
        return response
def admin_property_delete(request):
    if request.method=='GET':
        if isadmin(request):
            id=request.GET['id']
            property=Property.objects.get(id=id)
            cid=property.cid_id
            property.delete()
            response = HttpResponseRedirect('/admin_property_list/?cid=%s' % cid)
            return response
        else:
            return render(request, "adminlogin.html")
def admin_property_edit(request):
    if request.method=='GET':
        if isadmin(request):
            id = request.GET['id']
            property = Property.objects.get(id=id)
            return render(request, "admin_property_edit.html",{'property':property})
        else:
            return render(request, "adminlogin.html")
    if request.method == 'POST':
        id = request.POST['id']
        cid = request.POST['cid']
        name=request.POST['name']
        property = Property.objects.get(id=id)
        property.name=name
        property.save()
        response = HttpResponseRedirect('/admin_property_list/?cid=%s'%cid)
        return response
def admin_product_list(request):
    if request.method =='GET':
        if isadmin(request):
            cid = request.GET['cid']
            productlist=Product.objects.filter(cid_id=cid)
            plist=[]
            for i in productlist:
                product={'id':i.id,'name':i.name,'subTitle':i.subTitle,'orignalPrice':i.orignalPrice,
                         'promotePrice':i.promotePrice,'stock':i.stock}
                try:
                    pid = i.id
                    img=Productimage.objects.filter(typ="type_single",pid_id=pid)
                    id=img.first().id
                    product['img']='/static/img/productSingle/%s.jpg'%id
                except:
                    product['img'] = '/static/img/site/tmallbuy.png'
                plist.append(product)
            return render(request, "admin_product_list.html",{"plist":plist,"cid":cid})
        else:
            return render(request, "adminlogin.html")
def admin_product_add(request):
    if request.method=='POST':
        name=request.POST['name']
        subTitle=request.POST['subTitle']
        orignalPrice=request.POST['orignalPrice']
        promotePrice=request.POST['promotePrice']
        stock=request.POST['stock']
        cid=request.POST['cid']
        import django.utils.timezone as timezone
        createDate=timezone.now()
        Product.objects.create(name=name,subTitle=subTitle,orignalPrice=orignalPrice,promotePrice=promotePrice,stock=stock,createDate=createDate,cid_id=cid)
        # product=Product.objects.get(name=name)
        # pid=product.id
        # ptlist=Property.objects.filter(cid_id=cid)
        # for i in ptlist:
        #     ptv=Propertyvalue.objects.create(pid_id=pid,ptid_id=i.id)
        response = HttpResponseRedirect('/admin_product_list/?cid=%s' % cid)
        return response
def admin_product_delete(request):
    if request.method=='GET':
        if isadmin(request):
            id=request.GET['id']
            product=Product.objects.get(id=id)
            cid=product.cid_id
            product.delete()
            response = HttpResponseRedirect('/admin_product_list/?cid=%s' % cid)
            return response
        else:
            return render(request, "adminlogin.html")
def admin_product_edit(request):
    if request.method=='GET':
        if isadmin(request):
            id = request.GET['id']
            product = Product.objects.get(id=id)
            return render(request, "admin_product_edit.html",{'product':product})
        else:
            return render(request, "adminlogin.html")
    if request.method == 'POST':
        name = request.POST['name']
        subTitle = request.POST['subTitle']
        orignalPrice = request.POST['orignalPrice']
        promotePrice = request.POST['promotePrice']
        stock = request.POST['stock']
        cid = request.POST['cid']
        id=request.POST['id']
        product = Product.objects.get(id=id)
        product.name=name
        product.subTitle=subTitle
        product.orignalPrice=orignalPrice
        product.promotePrice=promotePrice
        product.stock=stock
        product.save()
        response = HttpResponseRedirect('/admin_product_list/?cid=%s'%cid)
        return response
def admin_product_editPropertyValue(request):
    if request.method=='GET':
        if isadmin(request):
            id = request.GET['id']
            product = Product.objects.get(id=id)
            cid=product.cid_id
            propertylist = Property.objects.filter(cid_id=cid)
            plist=[]
            for i in propertylist:
                try:
                    value=Propertyvalue.objects.get(pid_id=id,ptid_id=i.id).value
                except:
                    value=''
                property={'name':i.name,'value':value}
                plist.append(property)
            return render(request, "admin_product_editPropertyValue.html",{'propertylist':plist,'pid':id,'cid':cid})
        else:
            return render(request, "adminlogin.html")
    if request.method == 'POST':
        cid = request.POST['cid']
        pid=request.POST['pid']
        propertylist=Property.objects.filter(cid_id=cid)
        for i in propertylist:
            ptid=i.id
            value=request.POST[i.name]
            try:
                ptvalue=Propertyvalue.objects.get(pid_id=pid,ptid_id=ptid)
                ptvalue.value=value
                ptvalue.save()
            except:
                ptvalue=Propertyvalue(value=value, pid_id=pid, ptid_id=ptid)
                ptvalue.save()
        response = HttpResponseRedirect('/admin_product_list/?cid=%s'%cid)
        return response
def admin_productImage_list(request):
    if request.method == 'GET':
        if isadmin(request):
            pid=request.GET['pid']
            singlelist=Productimage.objects.filter(pid_id=pid,typ="type_single")
            slist = []
            for i in singlelist:
                single = {'id': i.id, 'typ': i.typ, 'img': '/static/img/productSingle/%s.jpg'%i.id}
                slist.append(single)
            detaillist=Productimage.objects.filter(pid_id=pid,typ="type_detail")
            dlist = []
            for i in detaillist:
                detail = {'id': i.id, 'typ': i.typ, 'img': '/static/img/productDetail/%s.jpg' % i.id}
                dlist.append(detail)
            return render(request, "admin_productImage_list.html",{'pid':pid,'slist':slist,'dlist':dlist})
        else:
            return render(request, "adminlogin.html")
def admin_productImage_add(request):
    if request.method=='POST':
        typ=request.POST['type']
        pid=request.POST['pid']
        file=request.FILES.get('file')
        if not file:
            return HttpResponse("no files for upload!")
        else:
            Productimage.objects.create(typ=typ,pid_id=pid)
            plist=Productimage.objects.filter(typ=typ,pid_id=pid)
            id=plist.last().id
            filename='%s.jpg'%id
            if typ=="type_single":
                path="./app/static/img/productSingle/"
            else:
                path="./app/static/img/productDetail/"
            save(file, path, filename)
            response = HttpResponseRedirect('/admin_productImage_list/?pid=%s'%pid)
            return response
def admin_productImage_delete(request):
    if request.method=='GET':
        if isadmin(request):
            id=request.GET['id']
            pid=request.GET['pid']
            img=Productimage.objects.get(id=id)
            typ=img.typ
            img.delete()
            if typ == "type_single":
                file = "./app/static/img/productSingle/%s.jpg"%id
            else:
                file = "./app/static/img/productDetail/%s.jpg"%id
            if os.path.exists(file):
                os.remove(file)
            else:
                return HttpResponse("no files")
            response = HttpResponseRedirect('/admin_productImage_list/?pid=%s'%pid)
            return response
        else:
            return render(request, "adminlogin.html")
def admin_order_list(request):
    if request.method =='GET':
        if isadmin(request):
            orderlist=Order.objects.all()
            olist=[]
            for i in orderlist:
                uid=i.uid_id
                user=User.objects.get(id=uid)
                name=user.name
                order={'id':i.id,'status':i.status,'user':name,'createDate':i.createDate,'payDate':i.payDate,
                       'deliveryDate':i.deliveryDate,'confirmDate':i.confirmDate}
                olist.append(order)
            return render(request, "admin_order_list.html",{"olist":olist})
        else:
            return render(request, "adminlogin.html")
def admin_user_list(request):
    if request.method =='GET':
        if isadmin(request):
            userlist=User.objects.all()
            return render(request, "admin_user_list.html",{'userlist':userlist})
        else:
            return render(request, "adminlogin.html")