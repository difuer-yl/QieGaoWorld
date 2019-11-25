import graphene
from graphene_django.types import DjangoObjectType
from QieGaoWorld.models import User, DeclareBuildings, Cases

class UserType(DjangoObjectType):
    class Meta:
        model=User

class CasesType(DjangoObjectType):
    class Meta:
        model=Cases

class BuildingsType(DjangoObjectType):
    class Meta:
        model=DeclareBuildings


class Query(graphene.ObjectType):
    all_cases=graphene.List(CasesType)
    all_buildings=graphene.List(BuildingsType)
    all_users=graphene.List(UserType)

    def resolve_all_cases(self,info,**kwargs):
        return Cases.objects.all()
    def resolve_all_users(self,info,**kwargs):
        return User.objects.all()