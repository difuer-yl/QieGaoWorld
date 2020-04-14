'''
@Author: chiaki
@Date: 2019-10-16 00:24:28
@LastEditors: chiaki
@LastEditTime: 2020-04-14 20:37:41
@Description: 
'''
from django.http import HttpResponse
import requests

from QieGaoWorld.views.decorator import check_post
from QieGaoWorld.views.dialog import dialog

from django.contrib.auth import logout


def logout(request):
    request.session['is_login'] = False
    request.session['username'] = ''
    request.session['password'] = ''

    rep=HttpResponse(dialog('ok', 'success', '登出成功'))
    rep.delete_cookie("qg_t",domain="qiegaoshijie.club")
    rep.delete_cookie("auto_login",domain="qiegaoshijie.club")
    requests.get("https://map.qiegaoshijie.club/test.php?type=logout")
    # logout(request)
    return rep
