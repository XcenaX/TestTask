from rest_framework.response import Response
from rest_framework.views import APIView

from main.serializers.user import UserSerializer
from main.serializers.company import CompanySerializer

from main.models import User, ChildCompany

from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class ChildCompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'post', 'delete']
    queryset = ChildCompany.objects.all()
    serializer_class = CompanySerializer