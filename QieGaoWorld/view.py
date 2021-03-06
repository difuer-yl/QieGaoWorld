import logging,json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count

from QieGaoWorld.views.announcement import announcement_list
from .views.declare import animals_list, buildings_list
from .views.decorator import check_login, check_post
from .views.settings import page_settings
from .views.ops import whitelist
from .views.wenjuan import problem_list
from .views import system,society,skull,task,user,declare,signin,ops,cms,demand,user,fish
from QieGaoWorld import parameter as Para 
from QieGaoWorld.models import DeclareBuildings, DeclareAnimals, Cases,Menu,Conf,SkullCustomize,Logs,Maps
from QieGaoWorld import common

from QieGaoWorld.views.police import username_get_nickname

from django.db.models import Count,Q

















# 使用协议
def agreement(request):
    return render(request, "agreement.html", {})


# 忘记密码
def forgotten(request):
    return render(request, "forgotten.html", {})


def global_settings(request):
    return {"PROJECT_VERSION": settings.PROJECT_VERSION,
            'AUTHOR': settings.PROJECT_VERSION}


def handle_uploaded_file(f):
    with open(f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@check_login
def user_center(request):
    announcements = announcement_list(request)

    MC_SERVER=Conf.objects.get(key="MC_SERVER").content

    na = len(DeclareAnimals.objects.all())
    nb = len(DeclareBuildings.objects.all())
    nc = len(Cases.objects.all())
    try:
        from mcstatus import MinecraftServer
        server = MinecraftServer.lookup(MC_SERVER)
        status = server.status()

        mot = status.description['text']
        motd = str(mot)
        pos = motd.find('§')
        while pos != -1:
            motd = motd[:pos] + motd[pos + 2:]
            pos = motd.find('§')

        fav = status.favicon
        opn = status.players.online
        user = []

        if status.players.sample is not None:
            for e in status.players.sample:
                user.append({'name': e.name, 'id': e.id,"nickname":username_get_nickname(e.name)})


        

        context = {
            'favicon': fav,
            'server_address': MC_SERVER,
            'online_players_list': user,
            'online_players_number': opn,
            'number_buildings': nb,
            'number_animals': na,
            'number_cases': nc,
            'permissions': request.session.get("permissions",""),
            'announcements': announcements,
            "latency":status.latency
        }
    except Exception as e:
        context = {
            'favicon': '',
            'server_address': MC_SERVER,
            'online_players_list': [],
            'online_players_number': '超时',
            'number_buildings': nb,
            'number_animals': na,
            'number_cases': nc,
            'permissions': request.session.get("permissions",""),
            'announcements': announcements,
            "latency":-1
        }
    return render(request, "dashboard/user_center.html", context)


@check_login
def page_announcement(request):
    announcements = announcement_list(request)
    print(announcements)
    content = {
        'announcements': announcements
    }
    return render(request, "dashboard/announcement/announcement.html", content)


@check_login
def page_declaration_center(request):
    # animals = animals_list(request, 'all')
    # buildings = buildings_list(request, 'all')
    if '%op%'  in request.session.get('permissions', ''):
        content = {
            'animals': DeclareAnimals.objects.count(),
            'buildings': DeclareBuildings.objects.count(),
            'skull': SkullCustomize.objects.count(),
            'maps': Maps.objects.count(),
            'permissions': request.session.get("permissions",""),
        }
    else:
        content = {
            'animals': DeclareAnimals.objects.count(),
            'buildings': DeclareBuildings.objects.count(),
            'permissions': request.session.get("permissions",""),
        }
    return render(request, "dashboard/declaration/center.html", content)


@check_login
def page_call_the_police(request):
    return render(request, "dashboard/police/call_the_police.html", {})


@check_login
def page_declare_animals(request):
    # my_animals = animals_list(request, 'user')
    content = {
        # 'my_animals': my_animals,
        'permissions': request.session.get("permissions",""),
    }
    return render(request, "dashboard/declaration/animals.html", content)


@check_login
def page_declare_buildings(request):
    # my_building = buildings_list(request, 'user')  # 这里选择获取当前登录用户的obj
    content = {
        # 'buildings': my_building,
        'permissions': request.session.get("permissions",""),
    }
    return render(request, "dashboard/declaration/buildings.html", content)


@check_login
def page_papers(request):
    return render(request, "dashboard/papers/papers.html", {})


@check_login
def page_community(request):
    return render(request, "dashboard/papers/community.html", {})


@check_login
def page_project_plan(request):
    return render(request, "dashboard/papers/plans.html", {})



@check_login
def page_world_map(request):
    return render(request, "dashboard/world_map/map.html", {})


@check_login
def page_rookies(request):
    return render(request, "dashboard/rookies/rookies.html", {})


@check_login
def dashboard(request):
    per=request.user.get_all_permissions()

    menu=Menu.objects.filter(Q(code__exact=None)|Q(code__in=per)).filter(status=True,type=1)
    
    
    parent_id=[]
    for m in menu:
        if m.parent not in parent_id:
            parent_id.append(m.parent)
    
    parent=Menu.objects.filter(status=True,id__in=parent_id).order_by("list")
    print(len(parent))
    # return 
    context = {
        'avatar': request.session.get("avatar",''),
        'nickname': request.session.get("nickname",''),
        'permissions': request.session.get("permissions",''),
        "menu":menu,
        "parent":parent
    }
    

    return render(request, "dashboard/dashboard.html", context)
@check_login
def page_whitelist(request):
    white_list=whitelist(request)
    context = {
        'list': white_list,
        'permissions': request.session.get("permissions",""),
        'len':len(white_list)
    }

    return render(request, "dashboard/ops/whitelist.html", context)

@check_login
def system_menu(request):
    per=request.user.get_all_permissions()

    menu=Menu.objects.filter(Q(code='')|Q(code__in=per))
    context = {
        'permissions': request.session.get("permissions",""),
        "menu":menu
    }

    return render(request, "dashboard/system/menu.html", context)
@check_login
def page_wenjuan(request):

    _type=Conf.objects.get(key="wenjuan_type")
    context = {
        'permissions': request.session.get("permissions",""),
        "wenjuan":problem_list(request),
        "type":json.loads(_type.content)
    }

    return render(request, "dashboard/wenjuan/wenjuan.html", context)


@check_login
def page_skull(request):
    
    context = {
        'permissions': request.session.get("permissions",""),
        # "skull":skull.skull_list(request)
    }

    return render(request, "dashboard/declaration/skull.html", context)

@check_login
def page_maps(request):
    # _list=declare.maps_list(request,"user")
    context = {
        'permissions': request.session.get("permissions",""),
        # "list":_list,
        # "page":common.page("maps",_list)
    }

    return render(request, "dashboard/declaration/maps.html", context)

@check_login
def page_para(request):
    
    context = {
        'permissions': request.session.get("permissions",""),
        "list":system.para_list(),
    }

    return render(request, "dashboard/system/parameter.html", context)

@check_login
def page_logs(request):
    

    context = {
        'permissions': request.session.get("permissions",""),
    }

    return render(request, "dashboard/system/logs.html", context)

@check_login
def page_society(request):
    
    context = {
        'permissions': request.session.get("permissions",""),
        "list":society.society_list()
    }

    return render(request, "dashboard/society/list.html", context)

def page_task_list(request):
    
    context = {
        'permissions': request.session.get("permissions",""),
        "list":task.task_list(request,True),
        "type":"list",
        "title":"任务列表"
    }

    return render(request, "dashboard/task/list.html", context)
def page_task(request):
    
    context = {
        'permissions': request.session.get("permissions",""),
        "list":task.task_list(request),
        "title":"我的任务"
    }

    return render(request, "dashboard/task/list.html", context)

def page_group_list(request):
    
    context = {
        'permissions': request.session.get("permissions",""),
        "list":user.group_list(request),
    }

    return render(request, "dashboard/system/group.html", context)
def page_rawerd(request):
    
    context = {
        'permissions': request.session.get("permissions",""),
        "list":signin.reward_list(request),
    }

    return render(request, "dashboard/signin/reward.html", context)
def page_signin(request):
    
    context = {
        'permissions': request.session.get("permissions",""),
    }

    return render(request, "dashboard/signin/logs.html", context)
def page_police_hall(request):
    
    context = {
        'permissions': request.session.get("permissions",""),
    }

    return render(request, "dashboard/police/police_hall.html", context)
def page_message(request):
    
    context = {
        "message":ops.message_list(request),
        'permissions': request.session.get("permissions",""),
    }

    return render(request, "dashboard/ops/message.html", context)
def page_ops_log(request):
    
    context = {
        'permissions': request.session.get("permissions",""),
    }

    return render(request, "dashboard/ops/log.html", context)
def cms_book_ist(request):
    
    context = {
        'permissions': request.session.get("permissions",""),
    }

    return render(request, "dashboard/cms/book.html", context)

@ensure_csrf_cookie
@check_login
@check_post
def dashboard_page(request):
    ensure_csrf_cookie(request)
    logging.info("Page Changed: " + request.POST.get("page", None))
    if request.POST.get("page", None) == "user_center":
        return user_center(request)

    if request.POST.get("page", None) == "announcement":
        return page_announcement(request)

    if request.POST.get("page", None) == "news":
        return render(request, "dashboard/settings/account.html", {})

    if request.POST.get("page", None) == "papers":
        return page_papers(request)

    if request.POST.get("page", None) == "project_plan":
        return page_project_plan(request)

    if request.POST.get("page", None) == "community":
        return page_community(request)

    if request.POST.get("page", None) == "declaration_center":
        return page_declaration_center(request)

    if request.POST.get("page", None) == "declare_buildings":
        return page_declare_buildings(request)

    if request.POST.get("page", None) == "declare_animals":
        return page_declare_animals(request)

    if request.POST.get("page", None) == "police_hall":
        return page_police_hall(request)

    if request.POST.get("page", None) == "call_the_police":
        return page_call_the_police(request)

    if request.POST.get("page", None) == "world_map":
        return page_world_map(request)

    if request.POST.get("page", None) == "rookies":
        return page_rookies(request)

    if request.POST.get("page", None) == "settings":
        return page_settings(request)
    if request.POST.get("page", None) == "whitelist":
        return page_whitelist(request)
    if request.POST.get("page", None) == "system_menu":
        return system_menu(request)
    if request.POST.get("page", None) == "wenjuan":
        return page_wenjuan(request)
    if request.POST.get("page", None) == "skull":
        return page_skull(request)
    if request.POST.get("page", None) == "maps":
        return page_maps(request)
    if request.POST.get("page", None) == "logs":
        return page_logs(request)
    if request.POST.get("page", None) == "para":
        return page_para(request)
    if request.POST.get("page", None) == "society":
        return page_society(request)
    if request.POST.get("page", None) == "society_info":
        return society.society_info(request)
    if request.POST.get("page", None) == "task_list":
        return page_task_list(request)
    if request.POST.get("page", None) == "task":
        return page_task(request)
    if request.POST.get("page", None) == "user":
        return user.user_list(request)
    if request.POST.get("page", None) == "group":
        return user.group(request)
    if request.POST.get("page", None) == "permissions":
        return user.permissions(request)
    if request.POST.get("page", None) == "reward":
        return page_rawerd(request)
    if request.POST.get("page", None) == "signin":
        return page_signin(request)
    if request.POST.get("page", None) == "message":
        return page_message(request)
    if request.POST.get("page", None) == "ops_log":
        return page_ops_log(request)
    if request.POST.get("page", None) == "cms_book_list":
        return cms_book_ist(request)
    if request.POST.get("page", None) == "cms_chapter_list":
        return cms.chapter(request)
    if request.POST.get("page", None) == "ops_log_list":
        return ops.log_info(request)
    if request.POST.get("page", None) == "demand_list":
        return demand.index(request,"list")
    if request.POST.get("page", None) == "demand":
        return demand.index(request)
    if request.POST.get("page", None) == "test":
        return user.test(request)
    if request.POST.get("page", None) == "fish":
        return fish.fish_index(request)
    if request.POST.get("page", None) == "rarity":
        return fish.rarity(request)
    if request.POST.get("page", None) == "fish_pond":
        return fish.pond(request)
    if request.POST.get("page", None) == "fish_pool":
        return fish.pool(request)
    if request.POST.get("page", None) == "fish_match":
        return fish.match(request)
    if request.POST.get("page", None) == "mc_icon":
        return fish.icon(request)

    return HttpResponse("Response: " + request.POST.get("page", None))
