'''
@Author: chiaki
@Date: 2019-10-16 00:24:28
@LastEditors: chiaki
@LastEditTime: 2020-03-22 13:00:34
@Description: 
'''
from django.http import HttpResponse

from QieGaoWorld.views.decorator import check_post
from QieGaoWorld.views.dialog import dialog

from django.contrib.auth import logout


def logout(request):
    request.session['is_login'] = False
    request.session['username'] = ''
    request.session['password'] = ''

    rep=HttpResponse(dialog('ok', 'success', '登出成功'))
    rep.delete_cookie("qg_t")
    rep.delete_cookie("auto_login")
    # logout(request)
    return rep
