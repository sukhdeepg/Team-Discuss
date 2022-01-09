from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Group, Subject
from .forms import GroupForm

def home(request):
    q = request.GET.get('q', '')

    groups = Group.objects.filter(
        Q(subject__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    group_count = groups.count()
    subjects = Subject.objects.all()

    context = {"groups": groups, "subjects": subjects, "group_count": group_count}
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