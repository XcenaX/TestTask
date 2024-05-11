from rest_framework import serializers
from main.models import ChildCompany
from django.core.exceptions import ObjectDoesNotExist


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildCompany
        fields = ('id', 'name', 'address', 'industry')


class ChildCompanyField(serializers.RelatedField):
    queryset = ChildCompany.objects.all()
    
    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        try:
            return ChildCompany.objects.get(id=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Компания с таким ID не найдена.')
        except TypeError:
            raise serializers.ValidationError('ID должен быть целым числом.')

