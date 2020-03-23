'''
@Author: chiaki
@Date: 2020-03-20 18:04:20
@LastEditors: chiaki
@LastEditTime: 2020-03-23 11:02:56
@Description: 
'''
import time
from QieGaoWorld import parameter
from django.http import HttpResponse

from QieGaoWorld.views.decorator import check_post
from QieGaoWorld.views.decorator import check_login
from QieGaoWorld.views.dialog import dialog
from QieGaoWorld.models import CmsBook, CmsChapter, Demand, DemandLike, Resolution, User
from QieGaoWorld import settings,common
from QieGaoWorld.common import diyrender;

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import os,traceback,uuid,logging,time,json,sys,requests
from QieGaoWorld.views.police import username_get_nickname,id_get_nickname
def url(request, s):
    return eval(s)(request)

def index(request,type=None) :
    return diyrender(request, 'dashboard/demand/index.html', {"type":type});

def list(request):
    operation=request.POST.get("type","user")
    page=request.POST.get("page",1)
    if operation == 'user':
        list=Demand.objects.filter(user_id=request.user.id).order_by("-like")
    else:
        list=Demand.objects.order_by("-like");
    paginator = Paginator(list, 25)
    list=paginator.get_page(page)
    id=[]
    status=[]
    if request.user.has_perm("QieGaoWorld.mayor"):
        status.append(0)
    if request.user.has_perm("QieGaoWorld.gwh"):
        status.append(1)
    if request.user.has_perm("QieGaoWorld.develop"):
        status.append(2)
    
    for i in range(0, len(list)):
        # list[i].time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(list[i].time))
        # user=User.objects.get(id=list[i].user_id)
        list[i].nickname = id_get_nickname(list[i].user_id)

        if list[i].status == 0:
            list[i].status_label = ''
            list[i].status_text = '待处理'
        elif list[i].status == 1:
            list[i].status_label = 'uk-label-success'
            list[i].status_text = '处理中'
        elif list[i].status == 2:
            list[i].status_label = 'uk-label-warning'
            list[i].status_text = '已完成'
        elif list[i].status == 3:
            list[i].status_label = 'uk-label-danger'
            list[i].status_text = '已拒绝'
        list[i].like_status=DemandLike.objects.filter(demand_id=list[i].id,user_id=request.session['id']).count()
        a={0:'',1:'',2:''}
        if len(status) > 0:
            res=Resolution.objects.filter(demand_id=list[i].id,user_id=request.user.id,type__in=status)
            for r in res:
                a.update({r.type:r})
        list[i].res=a


    return diyrender(request, 'dashboard/demand/list.html', {'list': list,"page":common.page("demand/list",list,operation),'type':operation})

def like(request):
    id=request.POST.get("id",None)
    status=int(request.POST.get("status",0))
    demand=Demand.objects.get(id=id)
    if status > 0:
        demand.lover("like")
        DemandLike.objects.filter(demand_id=id,user_id=request.user.id).delete()
    else :
        DemandLike.add(id,request.session['id'])
        demand.add('like')
    return HttpResponse(dialog('ok', 'success', ''))

def add(request):
    title=request.POST.get("title",None)
    content=request.POST.get("content",None)
    if len(title) <=0 or len(content) <=0:
        return HttpResponse(dialog('failed', 'danger', '标题或内容不能为空'))
    
    demand=Demand(title=title,details=content,user_id=request.session['id'])
    demand.save() 
    return HttpResponse(dialog('ok', 'success', '创建成功'))
    # else:
    #     return HttpResponse(dialog('failed', 'danger', '创建失败'))

def delete(request):
    id=request.POST.get("id",None)
    Demand.objects.get(id=id).delete()
    DemandLike.objects.filter(demand_id=id).delete()
    return HttpResponse(dialog('ok', 'success', '删除成功'))
    #TODO 决议
def resolution(request):

    id=request.POST.get("id",None)
    type=request.POST.get("type",None)
    content=request.POST.get("content",None)
    _type=['mayor','gwh','develop']
    if  request.user.has_perm("QieGaoWorld."+_type[int(type)]):
        demand=Demand.objects.get(id=id)
        if demand.status in [2,3]:
            return HttpResponse(dialog('failed', 'danger', '当前状态无法发表决议'))
        resolution=Resolution.objects.filter(user_id=request.user.id,demand_id=demand.id,type=type)
        if len(resolution) == 0:
            resolution=Resolution(user_id=request.user.id,type=type,content=content,demand_id=demand.id)
        else:
            resolution=resolution[0]
            resolution.content=content
        resolution.save()
        return HttpResponse(dialog('ok', 'success', '成功'))
    else:
        return HttpResponse(dialog('failed', 'danger', '权限不足'))
    #TODO 查看详情

def info(request):
    id=request.POST.get("id",None)
    demand=Demand.objects.get(id=id)
    
    resolution=['待处理','处理中','已完成','已拒绝','市长决议','糕委会决议','开发反馈']
    demand.status_label=resolution[demand.status]
    demand.nickname=User.objects.get(id=demand.user_id).nickname
    res=Resolution.objects.filter(demand_id=demand.id)
    for i in range(0,len(res)):
        res[i].type_label=resolution[(res[i].type+4)]
        res[i].nickname=User.objects.get(id=res[i].user_id).nickname
        
    return diyrender(request, "dashboard/demand/info.html", {"demand":demand,'resolution':resolution,"res":res})