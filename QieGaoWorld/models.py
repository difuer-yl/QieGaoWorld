from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractUser

from QieGaoWorld import settings

import django.utils.timezone as timezone

class User(AbstractUser):
    username = models.CharField(max_length=100,unique=True)  # 用户名
    password = models.CharField(max_length=100)  # 密码
    nickname = models.CharField(max_length=100)  # 昵称
    uuid = models.CharField(max_length=40, default='')  # uuid
    qqnumber = models.IntegerField(default=0)  # QQ号
    usrgroup = models.IntegerField(default=0)  # 用户组
    register_time = models.IntegerField(default=0)  # 注册时间
    token = models.CharField(default="",max_length=32)  # 自动登录
    token_expired_time = models.IntegerField(default=0)  # 自动登录
    avatar = models.CharField(max_length=1024, default='static\\media\\face\\default.jpg')  # 头像
    permissions = models.CharField(max_length=2048,
                                   default=settings.DEFAULT_PERMISSIONS)  # 权限
    USERNAME_FIELD="username"

    class Meta:
        permissions =(('all', u"查看所有列表"),
                      ('edit',u"编辑所有"),
                      )


# 报案记录
class Cases(models.Model):
    report_time = models.IntegerField(default=0)  # 报案时间
    position = models.CharField(max_length=1024)  # 案发地点
    coordinate = models.CharField(max_length=64)  # 精确坐标
    summary = models.CharField(max_length=1024)  # 案件简述
    detail = models.CharField(max_length=1024)  # 案件详细信息
    username = models.CharField(max_length=100)  # 报案者
    progress = models.CharField(max_length=100)  # 处理进度
    status = models.IntegerField(default=0)  # 案件结果（0:等待调查, 1:正在调查, 2:处理成功, 3:处理失败）
    picture = models.CharField(max_length=1024)  # 案发现场截图
    text=models.CharField(max_length=200)


# 建筑申报记录
class DeclareBuildings(models.Model):
    declare_time = models.IntegerField(default=0)  # 申请时间
    username = models.CharField(max_length=100, default='')  # 申请人用户名
    coordinate = models.CharField(max_length=64, default='')  # 建筑坐标
    area = models.CharField(max_length=64, default='')  # 建筑面积
    concept = models.CharField(max_length=1024, default='')  # 概念图
    plan = models.CharField(max_length=1024, default='')  # 平面图
    name = models.CharField(max_length=64, default='')  # 建筑名
    english_name = models.CharField(max_length=64, default='')  # 英文名
    summary = models.CharField(max_length=128, default='')  # 建筑简介
    detail = models.CharField(max_length=2048, default='')  # 建筑详细介绍
    perspective = models.CharField(max_length=1024, default='')  # 透视图
    predict_start_time = models.IntegerField(default=0)  # 预计开始时间
    predict_end_time = models.IntegerField(default=0)  # 预计结束时间
    actually_end_time = models.IntegerField(default=0)  # 实际结束时间

    status = models.IntegerField(default=0)  # 申报状态（0:挂起, 1:正在审核, 2:审核不通过, 3:审核通过, 4: 正在建设, 5:完工）
    type = models.IntegerField(default=0)  # 建筑类型（0:公共建筑, 1:私有建筑）
    text=models.CharField(max_length=200) #拒绝原因

    #宅基地自动登记
class Homestead(models.Model):
    time = models.IntegerField(default=0)  # 申请时间
    username = models.CharField(max_length=100, default='')  # 申请人用户名
    start_x = models.CharField(max_length=64, default='')  # 建筑坐标
    start_z = models.CharField(max_length=64, default='')  # 建筑坐标
    end_x = models.CharField(max_length=64, default='')  # 建筑坐标
    end_z = models.CharField(max_length=64, default='')  # 建筑坐标


# 动物申报记录
class DeclareAnimals(models.Model):
    declare_time = models.IntegerField(default=0)  # 申请时间
    username = models.CharField(max_length=100)  # 申请人
    binding = models.CharField(max_length=100)  # 隶属于（public为公共）
    license = models.CharField(max_length=64)  # 牌照号码
    feature = models.CharField(max_length=64)  # 特征
    status = models.IntegerField(default=0)  # 状态（0:未知, 1:存活, 2:丢失, 3:已死亡）


# 公告
class Announcement(models.Model):
    publish_time = models.IntegerField(default=0)  # 公告发布时间
    username = models.CharField(max_length=100)  # 公告发布者
    title = models.CharField(max_length=100)  # 公告标题
    content = models.CharField(max_length=512)  # 公告内容
    type = models.IntegerField(default=0)  # 公告类型（0:通知, 1:重要, 2:严重）
    visible = models.BooleanField(default=True)  # 公告是否可见

#
class Logs(models.Model):
    code=models.CharField(max_length=50) 
    text = models.TextField()
    time =models.IntegerField(default=0)

class Problem(models.Model):
    dry =models.CharField(max_length=500) #题干
    answer =models.CharField(max_length=200) #答案
    type =models.IntegerField()  #类型(0:填空，1：单选，2：多选，3：简答)
    status  =models.BooleanField(default=True) #是否启用
    list =models.IntegerField(default=0)

class ProblemInfo(models.Model):
    problem_id=models.IntegerField()
    content=models.TextField()
    status=models.BooleanField(default=True)

#菜单
class Menu(models.Model):
    name=models.CharField(max_length=50)
    type=models.IntegerField() #类型（0：目录，1：菜单）
    url=models.CharField(max_length=100)
    status=models.BooleanField(default=True)
    parent=models.IntegerField()
    code=models.CharField(default='',max_length=100)
    list=models.IntegerField(default=0)
class WenjuanLog(models.Model):
    user_id=models.IntegerField()
    problem_id=models.IntegerField()
    content=models.TextField()
class Conf(models.Model):
    key=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    content=models.TextField()
    
#头颅定制
class SkullCustomize(models.Model):
    user_id=models.IntegerField()
    content=models.TextField()
    number=models.IntegerField()
    status=models.BooleanField()
    name=models.CharField(max_length=50)

class Society(models.Model):
    name=models.CharField(max_length=50)
    sortname=models.CharField(max_length=10)
    abbreviation=models.CharField(max_length=10)
    type=models.IntegerField()
    banner = models.CharField(max_length=1024, default='')  
    detail = models.CharField(max_length=2048, default='')
    location = models.CharField(max_length=2048, default='')
    assets =models.TextField()
    member =models.TextField()
    manager =models.TextField()

#任务
class Task(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    username=models.CharField(max_length=100)
    status=models.IntegerField()  # 0：悬赏中 1：已完成  2：已结束

#地图
class Maps(models.Model):
    username=models.CharField(max_length=100)
    mapid=models.IntegerField()
    status=models.BooleanField()
    img=models.CharField(max_length=100)

#签到
class Signin(models.Model):
    username=models.CharField(max_length=100)
    day=models.IntegerField()
    year=models.IntegerField()
    month=models.IntegerField()
    reward=models.CharField(max_length=100)
    time=models.IntegerField(default=0)
    month_total=models.IntegerField(default=0)
    total=models.IntegerField(default=0)
    continuous=models.IntegerField(default=0)
    supplement=models.IntegerField(default=0)
#签到奖励
class Reward(models.Model):
    name=models.CharField(max_length=100)
    status=models.BooleanField(default=True)
    time=models.DateTimeField(default=timezone.now)
    start_time=models.CharField(max_length=20)
    end_time=models.CharField(max_length=20)
    type=models.CharField(max_length=20) # skull:头颅，map：地图
    mode=models.CharField(max_length=20)
    number=models.IntegerField(default=0)
    reward_id=models.TextField()
    release_mode =models.IntegerField(default=0)
    release_time =models.TextField()

class RewardMx(models.Model):
    
    number=models.IntegerField()
    
    reward_id=models.IntegerField(default=0)


class OtherData(models.Model):
    type=models.CharField(max_length=200) #数据类型
    name=models.CharField(max_length=200) #数据标识
    data=models.TextField() #数据

#公告
class Message(models.Model):
    content=models.TextField()
    num=models.IntegerField(default=300)
    status=models.BooleanField(default=True)




# #cms系统相关数据表
# class CmsCategory(models.Model):
#     title=models.CharField(max_length=100)

class CmsBook(models.Model):
    title = models.CharField(max_length=100)
    summary=models.CharField(max_length=200)
    author=models.CharField(max_length=100)
    img=models.CharField(max_length=250)
    show_time=models.IntegerField()
    status=models.BooleanField(default=True) #1已发布 0草稿箱 -1已删除 2已下架
    time=models.IntegerField()

class CmsChapter(models.Model):
    title=models.CharField(max_length=100)
    book_id=models.IntegerField(default=0)
    content=models.TextField()
    show_time=models.IntegerField()
    status=models.BooleanField(default=True) #1已发布 0草稿箱 -1已删除 2已下架
    time=models.IntegerField()


#需求表
class Demand(models.Model):
    title=models.CharField(max_length=100)#标题
    user_id=models.IntegerField() #关联用户id
    details=models.TextField() #详情
    status=models.IntegerField(default=0)#状态0待处理1处理中2已完成3已拒绝
    like=models.IntegerField(default=0)#点赞数

    def add(self,filed,num=1):
        # ob[filed] +=1
        setattr(self,filed,F(filed)+1)
        self.save()
        # do something with the book
    def lover(self,filed,num=1):
        setattr(self,filed,F(filed)-1)
        self.save()


#需求点赞表
#无需保留取消点赞记录所以使用硬删除
class DemandLike(models.Model):
    demand_id=models.IntegerField(default=0,null=False)#需求id
    user_id=models.IntegerField(default=0)#点赞用户id
    time=models.DateTimeField(auto_now_add=True)#点赞时间

    @classmethod
    def add(cls, demand_id,user_id):
        ob = cls(demand_id=demand_id,user_id=user_id)
        ob.save()
        # do something with the book
        return ob


class Resolution(models.Model):
    content=models.CharField(max_length=500)
    user_id=models.IntegerField(default=0,null=False)
    demand_id=models.IntegerField(default=0,null=False)
    type=models.IntegerField(default=0,null=False) #0市长决议1糕委会决议2开发反馈
    time=models.DateTimeField(auto_now=True)


#鱼池
class FishPond(models.Model):
    name=models.CharField(max_length=100)#名称
    status=models.BooleanField() #是否启用
    create_time=models.DateTimeField(auto_now_add=True)
    # fishs=models.ManyToManyField(Fish,related_name="pond_id",related_query_name="id")
    # def get_fish(self):
    #     return Fish.objects.filter(pond_id=self.id)
#稀有度
class Rarity(models.Model):
    name=models.CharField(max_length=100) #名称
    chance=models.FloatField() #爆率
    color=models.CharField(max_length=10)#颜色
    commands=models.TextField() #命令
    catch_announce=models.IntegerField() #广播距离 -1为全服
    status=models.IntegerField() #是否启用
    create_time=models.DateTimeField(auto_now_add=True)
#鱼







#鱼塘
class FishPool(models.Model):
    name=models.CharField(max_length=100)#名称
    type=models.IntegerField() #区域类型  1矩形 2圆形
    area=models.CharField(max_length=200) #区域数据 x1:z1:x2:z2 or x:z:r
    status=models.BooleanField() #是否启用
    create_time=models.IntegerField()

class Icon(models.Model):
    name=models.CharField(max_length=100)
    code=models.CharField(max_length=100,unique=True)
    icon=models.CharField(max_length=255)
    gif=models.CharField(max_length=255)
    status=models.BooleanField() #是否启用

class Fish(models.Model):
    name=models.CharField(max_length=100) #名称
    min=models.IntegerField() #最小尺寸
    max=models.IntegerField() #最大尺寸
    # rarity_id=models.IntegerField() #稀有度
    rarity=models.ForeignKey(Rarity,on_delete=models.DO_NOTHING)
    icon=models.ForeignKey(Icon,on_delete=models.DO_NOTHING,to_field="code",db_column="icon_code")
    # pond_id=models.IntegerField() #鱼池
    pond=models.ForeignKey(FishPond,on_delete=models.DO_NOTHING)
    icons=models.TextField() #icon相关
    commands=models.TextField() #触发命令
    conditions=models.TextField() #条件
    status=models.BooleanField() #是否启用
    create_time=models.DateTimeField(auto_now_add=True)

#鱼赛
class FishMatch(models.Model):
    name=models.CharField(max_length=100) #比赛名称
    start_time=models.IntegerField() #开始时间
    length=models.IntegerField() #持续时长
    type=models.IntegerField() #比赛类型 1周赛 2月赛 3季赛  4年赛 5其他
    pond_id=models.CharField(max_length=500) #鱼池id
    pool_id=models.CharField(max_length=500) #鱼塘id
    time=models.IntegerField()
