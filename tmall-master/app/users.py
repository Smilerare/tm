# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from app.models import User
#密码加密
def md5(str):
    import hashlib
    str=str.encode("utf-8")
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()
#登录界面
def login(request):
    if request.method == 'POST':
        name=request.POST['username']
        passwd=request.POST['password']
        passwd=md5(passwd)
        try:
            user=User.objects.get(name=name)
        except:
            return render(request, 'login.html',{'script':"alert",'wrong':'用户不存在'})
        if passwd==user.passwd:
            response = HttpResponseRedirect('/')
            response.set_cookie('name', name, 3600)
            return response
        else:
            return render(request, 'login.html',{'script':"alert",'wrong':'密码错误'})
    if request.method =='GET':
        return render(request, "login.html")
def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('name')
    return response
#注册错误提示、存入数据库
def regist(request):
    if request.method == 'POST':
        name=request.POST['username']
        email=request.POST['email']
        passwd=request.POST['password']
        passwd2 = request.POST['password2']
        try:
            user=User.objects.get(name=name)
            return render(request, 'regist.html', {'script': "alert", 'wrong': '用户已存在'})
        except:
            if passwd ==passwd2:
                passwd=md5(passwd)
                User.objects.create(name=name, passwd=passwd,email=email,isadmin=0)
                response = HttpResponseRedirect('/')
                response.set_cookie('name', name, 3600)
                return response
            else:
                return render(request, 'regist.html', {'script': "alert", 'wrong': '两次密码不一致'})
    if request.method =='GET':
        return render(request, "regist.html")