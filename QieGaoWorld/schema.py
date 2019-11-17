import graphene
import QieGaoWorld.user.schema

class Query(QieGaoWorld.user.schema.Query,graphene.ObjectType):
    pass

schema=graphene.Schema(query=Query)