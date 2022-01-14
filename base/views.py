from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group, Subject
from .forms import GroupForm

def login_user(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User not found.')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect.')

    context = {"page": page}
    return render(request, 'base/access.html', context)

def register_user(request):
    page = 'register'
    
    context = {"page": page}
    return render(request, 'base/access.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

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

@login_required(login_url='login')
def create_group(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}
    return render(request, 'base/create_group.html', context)

@login_required(login_url='login')
def update_group(request, pk):
    group = Group.objects.get(id=pk)
    form = GroupForm(instance=group)

    if request.user != group.moderator:
        return HttpResponse('Action not allowed.')

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}
    return render(request, 'base/create_group.html', context)

@login_required(login_url='login')
def delete_group(request, pk):
    group = Group.objects.get(id=pk)

    if request.user != group.moderator:
        return HttpResponse('Action not allowed.')

    if request.method == "POST":
        group.delete()
        return redirect('home')

    context = {"obj": group}
    return render(request, 'base/delete.html', context)