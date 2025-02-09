from csv import excel
from django.db.models import fields
from django.forms import ModelForm
from .models import Group
from django.contrib.auth.models import User

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['moderator', 'members']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']