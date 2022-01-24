from django.forms import fields
from rest_framework.serializers import ModelSerializer
from base.models import Group

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'