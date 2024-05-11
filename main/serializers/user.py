from rest_framework import serializers
from main.models import User
from django.core.exceptions import ObjectDoesNotExist

from main.serializers.role import RoleSerializer


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, required=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'roles')


class UserField(serializers.RelatedField):
    queryset = User.objects.all()
    
    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        try:
            return User.objects.get(id=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Пользователь с таким ID не найден.')
        except TypeError:
            raise serializers.ValidationError('ID должен быть целым числом.')

