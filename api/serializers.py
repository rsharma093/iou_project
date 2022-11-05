from rest_framework import serializers

from api.models import Users, Balance
from django.db.models import Sum


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    owes = serializers.SerializerMethodField()
    owed_by = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ('name', 'owes', 'owed_by', 'balance')

    def get_owes(self, obj):
        owes = {}
        for item in obj.owes.all():
            owes[item.lender.name] = item.amount

        return owes

    def get_owed_by(self, obj):
        owed_by = {}
        for item in obj.owed_by.all():
            owed_by[item.borrower.name] = item.amount

        return owed_by

    def get_balance(self, obj):
        total_owes = 0
        total_owed_by = 0
        if obj.owes.exists():
            total_owes = obj.owes.aggregate(Sum('amount'))['amount__sum']
        if obj.owed_by.exists():
            total_owed_by = obj.owed_by.aggregate(Sum('amount'))['amount__sum']

        return total_owed_by - total_owes


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ('borrower', 'lender', 'amount', 'expiration')
