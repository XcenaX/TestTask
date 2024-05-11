from rest_framework import serializers
from main.models import Contractor
from django.core.exceptions import ObjectDoesNotExist


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('id', 'name', 'service_domain', 'license_number')


class ContractorField(serializers.RelatedField):
    queryset = Contractor.objects.all()
    
    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        try:
            return Contractor.objects.get(id=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Подрядчик с таким ID не найден.')
        except TypeError:
            raise serializers.ValidationError('ID должен быть целым числом.')

