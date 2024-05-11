from rest_framework import serializers
from main.models import ContractAccess
from django.core.exceptions import ObjectDoesNotExist

from main.serializers.contract import ContractSerializer
from main.serializers.role import RoleSerializer
from main.serializers.user import UserSerializer


class ContractAccessSerializer(serializers.ModelSerializer):
    contract = ContractSerializer(many=False, required=True)
    user = UserSerializer(many=False, required=True)
    role = RoleSerializer(many=False, required=True)

    class Meta:
        model = ContractAccess
        fields = ('id', 'contract', 'user', 'role')


class ContractAccessField(serializers.RelatedField):
    queryset = ContractAccess.objects.all()
    
    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        try:
            return ContractAccess.objects.get(id=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Доступ к контракту с таким ID не найден.')
        except TypeError:
            raise serializers.ValidationError('ID должен быть целым числом.')

