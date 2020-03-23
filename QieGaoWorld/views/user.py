import re,json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import Group,Permission,GroupManager,PermissionManager,ContentType

from QieGaoWorld import parameter
from QieGaoWorld.views.decorator import check_post
from QieGaoWorld.views.decorator import check_login
from QieGaoWorld.views.dialog import dialog
from QieGaoWorld.models import User

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



from QieGaoWorld import settings,common

from django.db import connection

@check_login
@check_post
def url(request, s):
    return eval(s)(request)

#用户列表
def user_list(request):
    page=request.POST.get("page",1)
    list=User.objects.all();
    paginator = Paginator(list, 25)
    list=paginator.get_page(page)
    # user=User.objects.all()

    return common.diyrender(request, 'dashboard/system/user.html', {'list': list,"page":common.page("user/user_list",list)})

#用户组列表
def group(request):

    list=group_list(request)
    
    return common.diyrender(request, 'dashboard/system/group.html', {'list': list,"page":common.page("user/group",list)})

def group_list(request):
    group=Group.objects.all()
    for i in range(0,len(group)):
        group[i].value=group[i].name

    page=request.POST.get("page",1)
    list=Group.objects.all();
    paginator = Paginator(list, 25)
    list=paginator.get_page(page)
    return list;

def user_info(request):
    _id=(request.POST.get("id",None))
    user=User.objects.get(id=_id)
    list=group_list(request)
    l=['multiple',{'id':'','value':'请选择'}]
    for i in range(0,len(list)):
        a={
            'id':list[i].id,
            'value':list[i].name
        }
        l.append(a)
    cursor=connection.cursor()
    cursor.execute("select * from QieGaoWorld_user_groups where user_id="+_id+"")
    row=cursor.fetchall()
    group=[]
    for i in range(0,len(row)):
        if row[i][2] not in group:
            group.append(row[i][2]);

    return render(request, "dashboard/user/edit.html", {"info":user,"group":l,"user_group":group})

def user_edit(request):
    _id=int(request.POST.get("id",None))
    nikename=(request.POST.get("title",None))
    group=(request.POST.get("content",None))
    if '-' in group:
        group=group.split('-')
    user=User.objects.get(id=_id)
    user.nikename=nikename
    user.groups.clear()
    group_list=Group.objects.filter(id__in=group)
    user.groups.set(group_list)
    # for g in group:
    #     pass
    return HttpResponse(dialog('ok', 'success', '修改成功',{}))



#添加用户组
def group_add(request):
    _id=request.POST.get("id",None)
    name=request.POST.get("title")
    if _id==None or _id=='':
        group=Group(name=name)
    else:
        group=Group.objects.get(id=_id)
        group.name=name
    group.save()
    
    return HttpResponse(dialog('ok', 'success', '添加成功'))
#编辑用户组权限
def group_info(request):
    _id=request.POST.get("id",None)
    if _id == None:
        return HttpResponse(dialog('ok', 'danger', '参数错误'))
    per=Permission.objects.all()
    type=ContentType.objects.all();
    group=Group.objects.get(id=_id)
    m=[]
    # group_per=
    cursor=connection.cursor()
    cursor.execute("select * from auth_group_permissions where group_id="+_id+"")
    row=cursor.fetchall()
    group_per=[]
    for i in range(0,len(row)):
        if row[i][2] not in group_per:
            group_per.append(row[i][2]);
        

    # print(group_per)
    return render(request, "dashboard/system/group_info.html", {"per":per,"gp":group_per,"mode":m,"type":type,"group":group})
    
#编辑组权限
def group_permissions(request):
    _id=request.POST.get("id",None)
    status=request.POST.get("status",None)
    group=request.POST.get("group",None)
    group=Group.objects.get(id=group)
    permission=Permission.objects.get(id=_id)
    if status == 'true':
        print("add")
        group.permissions.add(permission)
    else: 
        group.permissions.remove(permission)
    # group.save()
    return HttpResponse(dialog('ok', 'success', '修改成功',{}))

#删除权限组
def group_del(request):
    _id=request.POST.get("id",None)
    Group.objects.get(id=_id).delete()
    return HttpResponse(dialog('ok', 'success', '删除成功',{}))

#权限列表
def permissions(request):
    

    per=Permission.objects.all()
    type=ContentType.objects.all();
    m=[]
    return render(request, "dashboard/system/permissions.html", {"per":per,"type":type})

#权限编辑
def permissions_edit(request):

    _id=request.POST.get("id",None)
    name=request.POST.get("title",None)
    code=request.POST.get("code",None)
    if _id == None or _id == '':
        permissions=Permission(name=name,codename=code)
    else:
        permissions=Permission.objects.get(id=_id)
        permissions.name=name
        permissions.codename=code
    permissions.save()
    return HttpResponse(dialog('ok', 'success', '修改成功',{}))

#权限删除
def permissions_del(request):
    _id=request.POST.get("id",None)
    Permission.objects.get(id=_id).delete()
    return HttpResponse(dialog('ok', 'success', '删除成功',{}))




def test(request):
    content_type=ContentType.objects.get_for_id(27)
    Permission.objects.create(codename='test',name="检测权限专用",content_type=content_type)
    # Permission.objects.create(codename='mayor',name="市长决议",content_type=content_type)
    # Permission.objects.create(codename='gwh',name="糕委会决议",content_type=content_type)
    # Permission.objects.create(codename='develop',name="开发反馈",content_type=content_type)
    return HttpResponse(dialog('ok', 'success', '成功',{}))

def generate_user(request):
    username=request.GET.get("u",None)
    if len(username)<3 :
         return
    with open(parameter.SPIGOT_PATH + "/plugins/WhiteList/config.yml", "r") as f:
        plays = f.read()
        if "- " + username.lower() not in plays:
            return HttpResponse(dialog('failed', 'danger', '您不在白名单'))

    with open(parameter.SPIGOT_PATH + "/banned-players.json", "rb") as f:
        plays = json.loads(f.read())
        s = "%"
        for b in plays:
            s += b['name'] + "%"
        if "%" + username + "%" in s:
            return HttpResponse(dialog('failed', 'danger', '登录失败！您的帐号已被此服务器封禁!'))
    cursor=connection.cursor()
    cursor.execute("select * from playertable where playername='"+username+"'")
    row=cursor.fetchone()
    if row ==None:
        return HttpResponse(dialog('failed', 'danger', '该账号不存在'))
    else:
        password=row[1]
    user = User.objects.get(username=username)
    if user is None :
        user = User(username=username, password=password, register_time=(time.time()))
    
    user.save()
    if not user.has_perm("QieGaoWorld.test") :
        
        user.groups.set(Group.objects.filter(id=3))

    
    rep=HttpResponse(dialog('ok', 'success', '登录成功',{"token":user.token}));
    return rep