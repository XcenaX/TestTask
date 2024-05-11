from rest_framework import serializers
from main.models import ContractRole
from django.core.exceptions import ObjectDoesNotExist


class RoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ContractRole
        fields = ('id', 'name', 'description')


class RoleField(serializers.RelatedField):
    queryset = ContractRole.objects.all()
    
    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        try:
            return ContractRole.objects.get(id=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Роль с таким ID не найдена.')
        except TypeError:
            raise serializers.ValidationError('ID должен быть целым числом.')

