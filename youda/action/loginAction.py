#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from service.UserService import UserService
from django.http.response import HttpResponse, HttpResponseRedirect
import json
from datetime import datetime
from django.utils.datastructures import MultiValueDictKeyError
from django.template import response
from apps.form import login

from PIL import Image, ImageFile
from apps.models import UsersAffiliate
from apps.CommonDao import CommonDao
def headUpload(request):
    return render_to_response('file_upload_test.html');

#常规处理方法，现将图片保存下来，然后处理
def readHeadFile(request):
    form = login(request.POST, request.FILES);
    if form.is_valid(): 
        print 'ok'
        f = request.FILES["imagefile"]  
        # des_origin_path 为你在服务器上保存原始图片的文件物理路径         
        des_origin_f = open("img1.jpg", "ab")  
        for chunk in f.chunks():  
            des_origin_f.write(chunk)  
        des_origin_f.close()
    return render_to_response();
#未保存之前处理
def readHeadFile2(request):
    form = login(request.POST, request.FILES);
    if form.is_valid(): 
        print 'ok'
        f = request.FILES["imagefile"]
        #title = request.POST["title"];
        cd = form.cleaned_data;#获得其他是数据
        title = cd["title"];
        print title;
        parser = ImageFile.Parser()  
        for chunk in f.chunks():  
            parser.feed(chunk)     
        img = parser.close()
        i2 = img.thumbnail((100,100))
        img.save("./static/image/head/t3.jpg");
    return render_to_response("file_upload_test.html");
 
def toLogin(request):
    '''
            登陆操作，记录用户的登陆状态（Session），设置Cookies
    '''
    if len(request.POST)==0:
        return render_to_response('login.html');#跳转到登陆页面
    else:#用户进行登陆操作
        request.session.set_expiry(0);#设置当浏览器关闭时，session失效
        try:
            user_name = request.POST['userName'];
            user_pass = request.POST['pass'];
            flag = request.POST['logintype']; 
        except MultiValueDictKeyError:
            return HttpResponseRedirect("/home/");
        userService = UserService();
        commonDao = CommonDao();
        user = userService.toLogin(user_name, user_pass,flag);
        mapo = {};
        if user:
            mapo['status'] =1;
            request.session['userId']=user.user_id;
            request.session['userName'] = user.user_name;
            request.session['updateTime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S");
            user_a = commonDao.toget(UsersAffiliate,user_id=user.user_id);
            school = user_a.school.all()[0]; 
            request.session['schoolId'] = school.school_id;
            request.session['schoolName'] = school.school_name;
        else:  
            mapo['status'] =-1;
        DATA = json.dumps(mapo);
        response = HttpResponse(DATA,content_type="application/json"); #json格式返回数据
        if user:
            response.set_cookie("USERNAME",user_name,60); #要加密储存
        return response;       
        #return HttpResponseRedirect("/loginpage/");