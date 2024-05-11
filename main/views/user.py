from rest_framework.response import Response
from rest_framework.views import APIView

from main.serializers.user import UserSerializer

from main.models import User

from django_filters.rest_framework import DjangoFilterBackend


from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение данных о пользователе",
        responses={200: UserSerializer},        
    )

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch']
    queryset = User.objects.select_related("role")
    serializer_class = UserSerializer
    
    def get_detail(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)