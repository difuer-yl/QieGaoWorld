'''
@Author: chiaki
@Date: 2019-10-16 00:24:28
@LastEditors: chiaki
@LastEditTime: 2020-03-23 21:33:08
@Description: 
'''
from django.shortcuts import render
from QieGaoWorld.views import login


# 使用此装饰器，请保证函数的第一个参数为request
def check_login(func):
    def wrapper(*args, **kw):
        # if not args[0].session.get('is_login', False):
        
        if not args[0].user.is_authenticated:
            
            return login._login_verify(args[0])
        else:
        #     if args[0].user.qqnumber ==0:
        #         return render(args[0], "error.html", {"error_message": "请前往服务器绑定QQ！","jump":"no"})
            args[0].session.set_expiry(3600)  # 1小时有效期
        return func(*args, **kw)

    return wrapper


# 使用此装饰器，请保证函数的第一个参数为request
def check_post(func):
    def wrapper(*args, **kw):
        if args[0].method != "POST":
            return render(args['request'], "error.html", {"error_message": "Request method invalid"})
        else:
            return func(*args, **kw)

    return wrapper
