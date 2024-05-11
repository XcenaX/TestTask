from main.serializers.role import RoleSerializer

from main.models import ContractRole

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'post', 'delete']
    queryset = ContractRole.objects.all()
    serializer_class = RoleSerializer