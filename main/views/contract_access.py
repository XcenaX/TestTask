from rest_framework.response import Response
from rest_framework.views import APIView

from main.serializers.contract_access import ContractAccessSerializer

from main.models import ContractAccess, User, ContractRole, Contract

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from main.permissions import IsMainRole

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ContractAccessViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    queryset = ContractAccess.objects.all()
    serializer_class = ContractAccessSerializer


class ContractAccessAPI(APIView):
    permission_classes = [IsMainRole]

    @swagger_auto_schema(
        operation_description="Добавляет доступ пользователя к контракту",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id', 'role_id'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID пользователя'),
                'role_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID роли')
            },
        ),
        responses={201: openapi.Response(description="Доступ к контракту добавлен")}
    )
    def post(self, request, contract_id):
        user_id = request.data.get("user_id")
        role_id = request.data.get("role_id")
        user = get_object_or_404(User, id=user_id)
        role = get_object_or_404(ContractRole, id=role_id)
        contract = get_object_or_404(Contract, id=contract_id)

        if ContractAccess.objects.filter(user=user, contract=contract).exists():
            return Response({"message": "У этого пользователя уже есть доступ к этому контракту!."}, status=status.HTTP_400_BAD_REQUEST)

        ContractAccess.objects.create(user=user, contract=contract, role=role)
        return Response({"message": "Доступ к контракту добавлен."}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Удаляет доступ пользователя к контракту",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description="ID пользователя", type=openapi.TYPE_INTEGER)
        ],
        responses={204: openapi.Response(description="Доступ к контракту удален")}
    )
    def delete(self, request, contract_id):
        user_id = request.query_params.get("user_id")
        contract_access = get_object_or_404(ContractAccess, contract_id=contract_id, user_id=user_id)
        contract_access.delete()
        return Response({"message": "Доступ к контракту удален."}, status=status.HTTP_204_NO_CONTENT)