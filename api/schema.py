import graphene

from graphene_django import DjangoObjectType
from api.models import Balance
import time


class BalanceType(DjangoObjectType):
    lender = graphene.String()
    borrower = graphene.String()

    class Meta:
        model = Balance
        fields = "__all__"

    def resolve_lender(self, info):
        return self.lender.name

    def resolve_borrower(self, info):
        return self.borrower.name


class Query(graphene.ObjectType):
    expire_ious = graphene.List(BalanceType)

    def resolve_expire_ious(self, info, **kwargs):
        return Balance.objects.filter(expiration__lt=time.time())


schema = graphene.Schema(query=Query)
