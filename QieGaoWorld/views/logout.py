from django.http import HttpResponse

from QieGaoWorld.views.decorator import check_post
from QieGaoWorld.views.dialog import dialog


def logout(request):
    request.session['is_login'] = False
    request.session['username'] = ''
    request.session['password'] = ''

    rep=HttpResponse(dialog('ok', 'success', '登出成功'))
    rep.delete_cookie("qg_t")
    return rep
