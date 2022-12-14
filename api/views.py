import ast
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action

from rest_framework import viewsets

from api.serializers import UsersSerializer, BalanceSerializer
from api.models import Users, Balance
from django.db.models import Sum


class UsersView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def get_queryset(self):
        users_list = self.request.query_params.get("users")
        if users_list:
            users_list = ast.literal_eval(users_list)
            return self.queryset.filter(name__in=users_list)
        else:
            return self.queryset


class BalanceView(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data["borrower"] = get_object_or_404(Users, name=data.get("borrower")).id
        data["lender"] = get_object_or_404(Users, name=data.get("lender")).id
        serializer = BalanceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        users = Users.objects.filter(
            id__in=[data.get("lender", ""), data.get("borrower", "")]
        )
        data = UsersSerializer(users, many=True).data

        return Response(data, status=status.HTTP_201_CREATED)
