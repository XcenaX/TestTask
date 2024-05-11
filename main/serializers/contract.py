from rest_framework import serializers
from main.models import Contract
from django.core.exceptions import ObjectDoesNotExist

from main.serializers.company import CompanySerializer
from main.serializers.contractor import ContractorSerializer
from main.serializers.role import RoleSerializer


class ContractSerializer(serializers.ModelSerializer):
    child_company = CompanySerializer(many=False, required=True)
    contractor = ContractorSerializer(many=False, required=True)
    roles = RoleSerializer(many=True, required=False)
    
    class Meta:
        model = Contract
        fields = ('id', 'name', 'description', 'child_company', 'contractor', 'roles', 'start_date', 'end_date', 'contract_document')


class ContractField(serializers.RelatedField):
    queryset = Contract.objects.all()
    
    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        try:
            return Contract.objects.get(id=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Контракт с таким ID не найден.')
        except TypeError:
            raise serializers.ValidationError('ID должен быть целым числом.')

