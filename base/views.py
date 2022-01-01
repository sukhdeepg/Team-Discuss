from django.shortcuts import render
from .models import Group

def home(request):
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, 'base/home.html', context)

def group(request, pk):
    group = Group.objects.get(id=pk)
    context = {"group": group}
    return render(request, 'base/group.html', context)