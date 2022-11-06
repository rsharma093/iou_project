from rest_framework import serializers

from api.models import Users, Balance


class UsersSerializer(serializers.ModelSerializer):
    owes = serializers.ReadOnlyField()
    owed_by = serializers.ReadOnlyField()
    balance = serializers.ReadOnlyField()

    class Meta:
        model = Users
        fields = ("name", "owes", "owed_by", "balance")


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ("borrower", "lender", "amount", "expiration")
