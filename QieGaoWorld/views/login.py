'''
@Description: In User Settings Edit
@Author: your name
@Date: 2018-09-14 23:31:44
@LastEditTime: 2020-06-09 13:16:48
@LastEditors: chiaki
'''
import json
import logging
import os
import time
import hashlib, uuid
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import connection

from django.contrib.auth import authenticate,login as _login


from QieGaoWorld import parameter
from QieGaoWorld import settings
from QieGaoWorld.models import User,Conf
# from django.contrib.auth.models import User
from QieGaoWorld.views.dialog import dialog
from QieGaoWorld import common,parameter
from django.contrib.auth.models import Group





# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# ajax (ensure csrf cookie)
# @ensure_csrf_cookie
def login(request):
    if request.session.get("is_login", False):
        return redirect("/dashboard")
    
    return render(request, "login.html", {"type":request.GET.get("t",''),"oauth_callback":request.GET.get("oauth_callback",'')})


def test(request):
    return render(request, "dialog.html", {})

def _login_verify(request):
    SPIGOT_PATH=Conf.objects.get(key="SPIGOT_PATH")
    # username=''
    # password=''
    t = str(request.COOKIES.get("qg_t", None))
    auto_login = str(request.COOKIES.get("auto_login", None))
    if auto_login=='true' and t != None and t != '':
        user=User.objects.filter(token=t).first()
        if user !=None:
            username=user.username
            password=user.password
        else:
            return render(request, "error.html", {"error_message": "您还未登录或登录状态已失效，请重新登录！!"})
    else:
        return render(request, "error.html", {"error_message": "您还未登录或登录状态已失效，请重新登录！"})
    with open(SPIGOT_PATH + "/plugins/WhiteList/config.yml", "r") as f:
        plays = f.read()
        if "- " + username.lower() not in plays:
            return render(request, "error.html", {"error_message": "登录失败！您的帐号不在白名单!"})
    

    with open(SPIGOT_PATH + "/banned-players.json", "rb") as f:
        plays = json.loads(f.read())
        s = "%"
        for b in plays:
            s += b['name'] + "%"
        if "%" + username + "%" in s:
            return render(request, "error.html", {"error_message": "登录失败！您的帐号已被此服务器封禁!"})


    uuid_ = get_uuid_from_name(username)  # 这里uuid_防止与uuid库名字冲突
    nickname = get_nickname_from_uuid(uuid_)
    user.uuid = uuid_
    # hashlib.md5()
    user.nickname = nickname
    # user.save()
    # if t == None or t == '':
    #     user.token_expired_time=int(time.time())
    #     md5_str=str(time.time())+user.username
    #     m2 = hashlib.md5()   
    #     m2.update(md5_str.encode('utf-8'))   
    #     user.token=m2.hexdigest()
    #检测用户是否有权限，没有权限加入普通用户权限组
    
    user.save()
    if not user.has_perm("QieGaoWorld.test") :
        
        user.groups.set(Group.objects.filter(id=3))

    # 登录成功后
    request.session["is_login"] = True
    request.session['username'] = user.username
    request.session['password'] = user.password
    request.session['nickname'] = user.nickname
    request.session['qqnumber'] = user.qqnumber
    request.session['usrgroup'] = user.usrgroup
    request.session['id'] = user.id
    request.session['register_time'] = user.register_time
    request.session['avatar'] = user.avatar
    request.session.set_expiry(3600)  # 1小时有效期
    

    with open(SPIGOT_PATH+"/ops.json", "r") as f:
        ops = f.read()
        a = (json.loads(ops))
        s = "%"
        for b in a:
            s += b['name'] + "%"
        if username in s:
            request.session['permissions'] = settings.OP_PERMISSIONS
        else:
            request.session['permissions'] = user.permissions
    
    rep=HttpResponse(dialog('ok', 'success', '登录成功',{"token":user.token}));
    rep= render(request, "login.html", {"type":request.GET.get("t",''),"oauth_callback":request.GET.get("oauth_callback",'')})
    _login(request,user)
    if auto_login == "true" :
        rep.set_cookie("qg_t",user.token)
        rep.set_cookie("auto_login",auto_login)
    else :
        rep.delete_cookie("qg_t")
        rep.delete_cookie("auto_login")
    # return rep
    return redirect("/dashboard")
# @api_view(['POST'])
def login_verify(request):

    SPIGOT_PATH=Conf.objects.get(key="SPIGOT_PATH")
    
    url = "./"
    username = str(request.POST.get("username", None))
    password = str(request.POST.get("password", None))
    # user=authenticate(username=username,password=password)
    # print(user.user_permissions)
    # return None
    t = str(request.POST.get("t", None))
    auto_login = str(request.POST.get("auto_login", None))
    if auto_login=='true' and t != None and t != '':
        _u=User.objects.filter(token=t).first()
        if _u !=None:
            username=_u.username
            password=_u.password
    password_md5 = hashlib.md5()   
    password_md5.update(password.encode('utf-8'))   
    cursor=connection.cursor()
    with open(SPIGOT_PATH + "/plugins/WhiteList/config.yml", "r") as f:
        plays = f.read()
        if "- " + username.lower() not in plays:
            return HttpResponse(dialog('failed', 'danger', '您不在白名单'))
            # return Response(dialog('failed', 'danger', '您不在白名单'))
    

    with open(SPIGOT_PATH + "/banned-players.json", "rb") as f:
        plays = json.loads(f.read())
        s = "%"
        for b in plays:
            s += b['name'] + "%"
        if "%" + username + "%" in s:
            return HttpResponse(dialog('failed', 'danger', '登录失败！您的帐号已被此服务器封禁!'))

    cursor.execute("select * from playertable where playername='"+username+"'")
    row=cursor.fetchone()
    if row ==None:
        return HttpResponse(dialog('failed', 'danger', '该账号不存在'))
    else :
        passwd=row[1]
    if ( password != passwd and  password_md5.hexdigest() != passwd ):
        return HttpResponse(dialog('failed', 'danger', '用户名或密码错误'))
    # try:
    #     user_url = "/plugins/ksptooi/fastlogin/database/"
    #     url = parameter.SPIGOT_PATH + user_url
    #     with open(url + username.lower() + ".gd", "r") as f:
    #         user = f.readline().strip()
    #         passwd = f.readline().strip()

    #         if passwd =='@Version=6':
    #             f.readline().strip()
    #             user = f.readline().strip()
    #             passwd = f.readline().strip()
    #             _username=username.lower()
    #         else:
    #             _username=username
    #     # user = User.objects.filter(username=username, password=password)
    # except IOError:
    #     return HttpResponse(dialog('failed', 'danger', '该账号不存在'))

    # if "playername=" + _username != user or ("password=" + password != passwd and "password=" + password_md5.hexdigest() != passwd ):
    #     return HttpResponse(dialog('failed', 'danger', '用户名或密码错误'))

    user = User.objects.get(username=username)
    if user is None :
        # User.objects.create_user(username,"",password)
        user = User(username=username, password=password, register_time=(time.time()))
        # obj.save()
        # user = User.objects.filter(username=username, password=password)
    # user = user[0]
    uuid_ = get_uuid_from_name(username)  # 这里uuid_防止与uuid库名字冲突
    nickname = get_nickname_from_uuid(uuid_)
    user.uuid = uuid_
    hashlib.md5()
    user.nickname = nickname
    # user.save()
    if t == None or t == '':
        user.token_expired_time=int(time.time())
        md5_str=str(time.time())+user.username
        m2 = hashlib.md5()   
        m2.update(md5_str.encode('utf-8'))   
        user.token=m2.hexdigest()
    #检测用户是否有权限，没有权限加入普通用户权限组
    
    user.save()
    if not user.has_perm("QieGaoWorld.test") :
        
        user.groups.set(Group.objects.filter(id=3))

    # 登录成功后
    request.session["is_login"] = True
    request.session['username'] = user.username
    request.session['password'] = user.password
    request.session['nickname'] = user.nickname
    request.session['qqnumber'] = user.qqnumber
    request.session['usrgroup'] = user.usrgroup
    request.session['id'] = user.id
    request.session['register_time'] = user.register_time
    request.session['avatar'] = user.avatar
    request.session.set_expiry(3600)  # 1小时有效期
    with open(SPIGOT_PATH+"/ops.json", "r") as f:
        ops = f.read()
        a = (json.loads(ops))
        s = "%"
        for b in a:
            s += b['name'] + "%"
        if username in s:
            request.session['permissions'] = settings.OP_PERMISSIONS
        else:
            # request.session['permissions'] = user.get_all_permissions()
        # else:
        #     if username == "Junyi99":  # 硬核编码（hhh
        #         request.session['permissions'] = settings.OP_PERMISSIONS
        #     else:
        #         request.session['permissions'] = user.permissions
            request.session['permissions'] = user.permissions
    
    rep=HttpResponse(dialog('ok', 'success', '登录成功',{"token":user.token}));
    _login(request,user)
    if auto_login == "true" :
        rep.set_cookie("qg_t",user.token,domain="qiegaoshijie.club")
        rep.set_cookie("auto_login",auto_login,domain="qiegaoshijie.club")
    else :
        rep.delete_cookie("qg_t",domain="qiegaoshijie.club")
        rep.delete_cookie("auto_login",domain="qiegaoshijie.club")
    return rep

def get_uuid_from_name(name):
    player_name = "OfflinePlayer:%s" % name
    m = hashlib.md5()
    m.update(player_name.encode("utf-8"))
    d = bytearray(m.digest())
    d[6] &= 0x0f
    d[6] |= 0x30
    d[8] &= 0x3f
    d[8] |= 0x80
    return (uuid.UUID(bytes=bytes(d)))


def get_nickname_from_uuid(uuid):
    SPIGOT_PATH=Conf.objects.get(key="SPIGOT_PATH")
    try:
        with open(SPIGOT_PATH+("/plugins/Essentials/userdata/%s.yml" % uuid)) as f:
            lines = f.readlines()
            for l in lines:
                if "nickname: " in l:
                    return l[9:len(l) - 1]
            return ""
    except IOError:
        return ""

def auto_login(request):
    

    token = str(request.GET.get("token", None))
    

    # user = User.objects.filter(token_expired_time__gte=int(time.time()), token=token)
    user = User.objects.filter(token=token)
    if len(user) == 0:
        return HttpResponse(dialog('failed', 'danger', '用户名或密码错误'))
    else:
        user = user[0]

    # 登录成功后
    data={}
    data["is_login"] = True
    data['username'] = user.username
    data['nickname'] = user.nickname
    data['qqnumber'] = user.qqnumber
    data['usrgroup'] = user.usrgroup
    data['id'] = user.id
    data['register_time'] = user.register_time
    data['avatar'] = user.avatar
    # data.set_expiry(3600)  # 1小时有效期


    return HttpResponse(dialog('ok', 'success', '登录成功',data))

