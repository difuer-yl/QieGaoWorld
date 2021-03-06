'''
@Author: chiaki
@Date: 2020-07-03 22:57:18
@LastEditors: chiaki
@LastEditTime: 2020-08-02 00:02:52
@Description: 
'''

import json,datetime
from django.shortcuts import render
from django.http import HttpResponse

from QieGaoWorld.models import Fish,FishPond,FishPool,Rarity,Icon,FishMatch
from QieGaoWorld.views.dialog import dialog
from QieGaoWorld.views.decorator import check_post
from QieGaoWorld.views.decorator import check_login





@check_login
@check_post
def url(request, s):
    return eval(s)(request)

#鱼相关
def fish_index(request):

    fish_list=Fish.objects.all()
    rarity_list=Rarity.objects.filter(status=1)
    pond_list=FishPond.objects.filter(status=1)
    icons=Icon.objects.all()
    # for i in range(0,len(fish_list)):
    #     icon=json.loads(fish_list[i].icon)
    #     if(icon['id'] != ""):
    #         if(icons.get(icon['id'],None) != None):
    #             fish_list[i]['icons']=icons.get(icon['id'])
    #         else:
    #             icon_=Icon.objects.filter(name=icon['id'])[0]
    #             fish_list[i].icons=icon_
    #             icons[icon['id']]=icon_

    return render(request, 'dashboard/fish/fish.html', {"list":fish_list,"rarity":rarity_list,"pond":pond_list,'icons':icons})

def fish_edit(request):
    name=request.POST.get("name","")
    if name == "":
        return HttpResponse(dialog('failed', 'danger', '请填写名称!'))
    min=request.POST.get("min","")
    max=request.POST.get("max","")
    rarity_id=request.POST.get("rarity","")
    if min == "" or max == "":
        return HttpResponse(dialog('failed', 'danger', '请填写尺寸范围!'))
    if rarity_id == "":
        return HttpResponse(dialog('failed', 'danger', '请选择稀有度!'))
    pond_id=request.POST.get("pond","")
    # if min == "" or max == "":
    #     return HttpResponse(dialog('failed', 'danger', '请填写尺寸范围!'))
    icon_id=request.POST.get("icon","")
    if icon_id == "":
        return HttpResponse(dialog('failed', 'danger', '请选择图标!'))
    # icon=Icon.objects.get(id=icon_id);
    commands=request.POST.get("commands","")
    icons=request.POST.get("icons","")
    conditions=request.POST.get("conditions",0)
    _id=request.POST.get("id","")

    if _id == "":
        info=Fish(name=name,status=1,min=min,max=max,commands=commands,rarity_id=rarity_id,icon_id=icon_id,conditions=conditions,pond_id=pond_id,icons=icons)
    else:
        info=Fish.objects.get(id=_id)
        info.name=name
        info.conditions=conditions 
        info.icon_id=icon_id
        info.commands=commands
        info.rarity_id=rarity_id 
        info.max=max 
        info.min=min 
        info.pond_id=pond_id 
        info.icons=icons 
    
    info.save()
    return HttpResponse(dialog('ok', 'success', '保存成功!'))

def fish_del(request):
    if "%op%" not in request.session.get('permissions', ''):
        return HttpResponse(dialog('failed', 'danger', '权限不足!'))
    id=request.POST.get('id',None)
    reward=Fish.objects.get(id=id)
    
    reward.delete()
    return HttpResponse(dialog('ok', 'success', '删除成功!'))

def fish_status(request):
    if "%op%" not in request.session.get('permissions', ''):
        return HttpResponse(dialog('failed', 'danger', '权限不足!'))
    status=str( request.POST.get('status',None))
    id=request.POST.get('id',None)
    menu=Fish.objects.get(id=id)
    
    if(status == "True"):
        menu.status=False
    else:
        menu.status=True
    menu.save()
    return HttpResponse(dialog('ok', 'success', 'ok!'))

#稀有度相关
def rarity(request):

    list=Rarity.objects.all()

    return render(request, 'dashboard/fish/rarity.html', {"list":list})

def rarity_edit(request):
    name=request.POST.get("name","")
    if name == "":
        return HttpResponse(dialog('failed', 'danger', '请填写名称!'))
    chance=request.POST.get("chance",0)
    color=request.POST.get("color","")
    # number=request.POST.get("number","")
    if chance == "":
        return HttpResponse(dialog('failed', 'danger', '请填写爆率!'))
    if color == "":
        return HttpResponse(dialog('failed', 'danger', '请填写颜色!'))
    commands=request.POST.get("commands","")
    catch_announce=request.POST.get("catch_announce",0)
    if(catch_announce == ''):
        catch_announce=0

    
    _id=request.POST.get("id","")
    if _id == "":
        info=Rarity(name=name,status=1,chance=chance,color=color,commands=commands,catch_announce=catch_announce)
    else:
        info=Rarity.objects.get(id=_id)
        info.name=name
        info.chance=chance 
        info.color=color
        info.commands=commands
        info.catch_announce=catch_announce 
    
    info.save()
    return HttpResponse(dialog('ok', 'success', '保存成功!'))

def rarity_del(request):
    if "%op%" not in request.session.get('permissions', ''):
        return HttpResponse(dialog('failed', 'danger', '权限不足!'))
    id=request.POST.get('id',None)
    reward=Rarity.objects.get(id=id)
    
    reward.delete()
    return HttpResponse(dialog('ok', 'success', '删除成功!'))

def rarity_status(request):
    if "%op%" not in request.session.get('permissions', ''):
        return HttpResponse(dialog('failed', 'danger', '权限不足!'))
    status=str( request.POST.get('status',None))
    id=request.POST.get('id',None)
    menu=Rarity.objects.get(id=id)
    
    if(status == "True"):
        menu.status=False
    else:
        menu.status=True
    menu.save()
    return HttpResponse(dialog('ok', 'success', 'ok!'))

#鱼池
def pond(request):

    list=FishPond.objects.all()

    return render(request, 'dashboard/fish/pond.html', {"list":list})

def pond_edit(request):
    name=request.POST.get("name","")
    if name == "":
        return HttpResponse(dialog('failed', 'danger', '请填写名称!'))
    
    _id=request.POST.get("id","")
    if _id == "":
        info=FishPond(name=name,status=1)
    else:
        info=FishPond.objects.get(id=_id)
        info.name=name
    
    info.save()
    return HttpResponse(dialog('ok', 'success', '保存成功!'))

def pond_del(request):
    if "%op%" not in request.session.get('permissions', ''):
        return HttpResponse(dialog('failed', 'danger', '权限不足!'))
    id=request.POST.get('id',None)
    reward=FishPond.objects.get(id=id)
    
    reward.delete()
    return HttpResponse(dialog('ok', 'success', '删除成功!'))

def pond_status(request):
    if "%op%" not in request.session.get('permissions', ''):
        return HttpResponse(dialog('failed', 'danger', '权限不足!'))
    status=str( request.POST.get('status',None))
    id=request.POST.get('id',None)
    menu=FishPond.objects.get(id=id)
    
    if(status == "True"):
        menu.status=False
    else:
        menu.status=True
    menu.save()
    return HttpResponse(dialog('ok', 'success', 'ok!'))


#图标
def icon(request):

    list=Icon.objects.all()

    return render(request, 'dashboard/fish/icon.html', {"list":list})

def icon_edit(request):
    name=request.POST.get("name","")
    if name == "":
        return HttpResponse(dialog('failed', 'danger', '请填写名称!'))
    code=request.POST.get("code","")
    if code == "":
        return HttpResponse(dialog('failed', 'danger', '请填写标识!'))
    icon=request.POST.get("icon","")
    if icon == "":
        return HttpResponse(dialog('failed', 'danger', '请填写静态图!'))
    gif=request.POST.get("gif","")
    if gif == "":
        return HttpResponse(dialog('failed', 'danger', '请填写动态图!'))
    
    _id=request.POST.get("id","")
    if _id == "":
        info=Icon(name=name,status=1,gif=gif,icon=icon,code=code)
    else:
        info=Icon.objects.get(id=_id)
        info.name=name
        info.gif=gif
        info.icon=icon
        info.code=code
    
    info.save()
    return HttpResponse(dialog('ok', 'success', '保存成功!'))

def icon_del(request):
    if "%op%" not in request.session.get('permissions', ''):
        return HttpResponse(dialog('failed', 'danger', '权限不足!'))
    id=request.POST.get('id',None)
    info=Icon.objects.get(id=id)
    
    info.delete()
    return HttpResponse(dialog('ok', 'success', '删除成功!'))

def icon_status(request):
    if "%op%" not in request.session.get('permissions', ''):
        return HttpResponse(dialog('failed', 'danger', '权限不足!'))
    status=str( request.POST.get('status',None))
    id=request.POST.get('id',None)
    info=Icon.objects.get(id=id)
    
    if(status == "True"):
        info.status=False
    else:
        info.status=True
    info.save()
    return HttpResponse(dialog('ok', 'success', 'ok!'))


#比赛
def match(request):

    list=FishMatch.objects.all()
    for i in range(0,len(list)):
        list[i].start_time=(datetime.datetime.fromtimestamp(list[i].start_time))
        list[i].type=('','周赛','月赛','季赛','年赛','其他')[int(list[i].type)]
    pond=FishPond.objects.filter(status=1)
    pool=FishPool.objects.filter(status=1)
        

    return render(request, 'dashboard/fish/match.html', {"list":list,"pond":pond,"pool":pool})

def match_edit(request):
    name=request.POST.get("name","")
    if name == "":
        return HttpResponse(dialog('failed', 'danger', '请填写名称!'))
    start_time=request.POST.get("start_time","")
    start_time=datetime.datetime.fromisoformat(start_time).timestamp()
    if start_time == "":
        return HttpResponse(dialog('failed', 'danger', '请填写开始时间!'))
    length=request.POST.get("length","")
    if length == "":
        return HttpResponse(dialog('failed', 'danger', '请填写时长!'))
    pond_id=request.POST.getlist("pond_id[]","")
    pond_id=",".join(pond_id)
    if pond_id == "":
        return HttpResponse(dialog('failed', 'danger', '请填写启用鱼池!'))
    pool_id=request.POST.getlist("pool_id[]","")
    pool_id=",".join(pool_id)
    if pool_id == "":
        return HttpResponse(dialog('failed', 'danger', '请填写启用鱼塘!'))
    
    _id=request.POST.get("id","")
    if _id == "":
        info=FishMatch(name=name,start_time=start_time,length=length,pond_id=pond_id,pool_id=pool_id)
    else:
        info=FishMatch.objects.get(id=_id)
        info.start_time=start_time
        info.length=length
        info.pond_id=pond_id
        info.pool_id=pool_id
        info.name=name
    
    info.save()
    return HttpResponse(dialog('ok1', 'success', '保存成功!'))

def match_del(request):
    if "%op%" not in request.session.get('permissions', ''):
        return HttpResponse(dialog('failed', 'danger', '权限不足!'))
    id=request.POST.get('id',None)
    info=FishMatch.objects.get(id=id)
    
    info.delete()
    return HttpResponse(dialog('ok', 'success', '删除成功!'))

def match_status(request):
    if "%op%" not in request.session.get('permissions', ''):
        return HttpResponse(dialog('failed', 'danger', '权限不足!'))
    status=str( request.POST.get('status',None))
    id=request.POST.get('id',None)
    info=Icon.objects.get(id=id)
    
    if(status == "True"):
        info.status=False
    else:
        info.status=True
    info.save()
    return HttpResponse(dialog('ok', 'success', 'ok!'))

#鱼塘
def pool(request):

    list=FishPool.objects.all()
    for i in range(0,len(list)):
        list[i].type=('','矩形','圆形')[int(list[i].type)]
        

    return render(request, 'dashboard/fish/pool.html', {"list":list})

def pool_edit(request):
    name=request.POST.get("name","")
    if name == "":
        return HttpResponse(dialog('failed', 'danger', '请填写名称!'))
    type=request.POST.get("type","")
    if type == "":
        return HttpResponse(dialog('failed', 'danger', '清选择类型!'))
    area=request.POST.get("area","")
    if area == "":
        return HttpResponse(dialog('failed', 'danger', '请填写区域!'))
    
    _id=request.POST.get("id","")
    if _id == "":
        info=FishPool(name=name,type=type,status=1,area=area)
    else:
        info=FishPool.objects.get(id=_id)
        info.type=type
        info.area=area
        info.name=name
    
    info.save()
    return HttpResponse(dialog('ok', 'success', '保存成功!'))

def pool_del(request):
    if "%op%" not in request.session.get('permissions', ''):
        return HttpResponse(dialog('failed', 'danger', '权限不足!'))
    id=request.POST.get('id',None)
    info=FishPool.objects.get(id=id)
    
    info.delete()
    return HttpResponse(dialog('ok', 'success', '删除成功!'))

def pool_status(request):
    if "%op%" not in request.session.get('permissions', ''):
        return HttpResponse(dialog('failed', 'danger', '权限不足!'))
    status=str( request.POST.get('status',None))
    id=request.POST.get('id',None)
    info=FishPool.objects.get(id=id)
    
    if(status == "True"):
        info.status=False
    else:
        info.status=True
    info.save()
    return HttpResponse(dialog('ok', 'success', 'ok!'))
