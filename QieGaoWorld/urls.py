'''
@Author: chiaki
@Date: 2019-11-25 23:21:33
@LastEditors: chiaki
@LastEditTime: 2020-07-04 10:57:07
@Description: 
'''
"""QieGaoWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.urls import path
from . import view
from .views import login, logout
from .views import avatar, police
from .views import declare, register,ops,system,wenjuan,skull,society,task,user,signin,cms,api,demand,fish
from .views import announcement
# from graphene_django.views import GraphQLView


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # path("login",)
    url(r'^$', login.login),

    url(r"^login$", login.login),
    url(r"^autologin$", login.auto_login),
    url(r"^logout$", logout.logout),
    url(r"^login_verify$", login.login_verify),

    url(r"^register$", register.register),
    url(r"^register_verify$", register.register_verify),


    url(r"^forgotten$", view.forgotten),
    url(r"^agreement$", view.agreement),
    url(r"^dashboard$", view.dashboard),

    url(r"^upload_face$", avatar.avatar_upload),
    url(r"^upload_building_plan$", declare.upload_building_plan),
    url(r"^upload_building_concept$", declare.upload_building_concept),
    url(r"^upload_building_perspective$", declare.upload_building_perspective),

    url(r"^dashboard\/page$", view.dashboard_page),
    # TODO: 完善 Save Changes
    # url(r"^save_changes$", view.save_changes),
    url(r"^police_report$", police.report),
    url(r"^police_change_status$", police.change_status),
    url(r"^police_case_detail$", police.case_detail),
    url(r"^police/police_list$", police.police_list),
    # url(r"^admin$", view.admin),
    # url(r"^admin_login_verify$", view.admin_login_verify),
    # url(r"^admin\/dashboard$", view.admin_dashboard),
    

    url(r"^animals_add$", declare.animals_add),
    url(r"^animals_change_status$", declare.animals_change_status),

    url(r"^buildings_add$", declare.buildings_add),
    url(r"^buildings_detail$", declare.buildings_detail),
    url(r"^buildings_change_status$", declare.buildings_change_status),

    url(r"^announcement_new$", announcement.announcement_new),
    url(r"^announcement_delete$", announcement.announcement_delete),
    url(r"^test", login.test),
    path("skull/<str:s>", skull.url),
    path("declare/<str:s>", declare.url),
    path("ops/<str:s>", ops.url),
    path("system/<str:s>", system.url),
    path("wenjuan/<str:s>", wenjuan.url),
    path("society/<str:s>", society.url),
    path("task/<str:s>", task.url),
    path("user/<str:s>", user.url),
    path("signin/<str:s>", signin.url),
    path("cms/<str:s>", cms.url),
    path("api/<str:s>", api.url),
    path("demand/<str:s>", demand.url),
    path("fish/<str:s>", fish.url),
    # path("graphql", GraphQLView.as_view(graphiql=True)),
]
