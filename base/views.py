from django.shortcuts import render, redirect
from .models import Group
from .forms import GroupForm

def home(request):
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, 'base/home.html', context)

def group(request, pk):
    group = Group.objects.get(id=pk)
    context = {"group": group}
    return render(request, 'base/group.html', context)

def create_group(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}
    return render(request, 'base/create_group.html', context)

def update_group(request, pk):
    group = Group.objects.get(id=pk)
    form = GroupForm(instance=group)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}
    return render(request, 'base/create_group.html', context)

def delete_group(request, pk):
    group = Group.objects.get(id=pk)
    if request.method == "POST":
        group.delete()
        return redirect('home')

    context = {"obj": group}
    return render(request, 'base/delete.html', context)