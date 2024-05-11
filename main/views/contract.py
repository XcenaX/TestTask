from rest_framework.response import Response
from rest_framework.views import APIView

from main.serializers.contract import ContractSerializer
from main.serializers.user import UserSerializer

from main.models import Contract, ContractAccess, User

from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q


class ContractViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    serializer_class = ContractSerializer
    queryset = Contract.objects.select_related('child_company', 'contractor').prefetch_related('roles')

    def list(self, request, *args, **kwargs):
        """
        Получение списка контрактов, к которым пользователь имеет доступ.
        """
        user = request.user
        
        direct_access_contracts = ContractAccess.objects.filter(user=user).values_list('contract_id', flat=True)
        role_access_contracts = Contract.objects.filter(roles__in=user.roles.all()).values_list('id', flat=True)

        accessible_contract_ids = set(direct_access_contracts) | set(role_access_contracts)

        queryset = Contract.objects.filter(id__in=accessible_contract_ids).distinct()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Получение контракта по id. Можно получить только контракт к которому есть доступ
        """
        contract = self.get_object()
        user = request.user
        
        has_direct_access = ContractAccess.objects.filter(contract=contract, user=user).exists()
        has_role_access = contract.roles.filter(id__in=user.roles.all()).exists()

        if not (has_direct_access or has_role_access):
            return Response({'error': 'У вас нет доступа к этому контракту'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(contract)
        return Response(serializer.data)
    

class ContractUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, contract_id):
        """
        Возвращает список пользователей, работающих с договором.
        """
        if not Contract.objects.filter(id=contract_id).exists():
            return Response({'error': 'Контракт не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        contract = Contract.objects.get(id=contract_id)

        has_direct_access = ContractAccess.objects.filter(contract=contract, user=request.user).exists()
        has_role_access = contract.roles.filter(id__in=request.user.roles.all()).exists()

        if not (has_direct_access or has_role_access):
            return Response({'error': 'У вас нет доступа к этому контракту'}, status=status.HTTP_403_FORBIDDEN)

        users = ContractAccess.objects.filter(contract_id=contract_id).select_related('user').values_list('user', flat=True)
        
        users_qs = User.objects.filter(id__in=users)
        serializer = UserSerializer(users_qs, many=True)
        
        return Response(serializer.data)