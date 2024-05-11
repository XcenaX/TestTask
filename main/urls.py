from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views.user import UserViewSet, UserDetail
from main.views.auth import Login, Register
from main.views.company import ChildCompanyViewSet
from main.views.contract_access import ContractAccessViewSet, ContractAccessAPI
from main.views.contract import ContractViewSet, ContractUsersAPIView
from main.views.contractor import ContractorViewSet
from main.views.role import RoleViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'child-companies', ChildCompanyViewSet)
# router.register(r'contractors', ContractorViewSet)
# router.register(r'contract-accesses', ContractAccessViewSet)
router.register(r'contracts', ContractViewSet)
# router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('user/', UserDetail.as_view(), name='user_detail'),

    path('contracts/<int:contract_id>/users/', ContractUsersAPIView.as_view(), name='contract_users'),

    path('contracts/<int:contract_id>/access/', ContractAccessAPI.as_view(), name='contract-access'),

    path('auth/login/', Login.as_view(), name='login'),
    path('auth/register/', Register.as_view(), name='register'),

    path('', include(router.urls)),
]