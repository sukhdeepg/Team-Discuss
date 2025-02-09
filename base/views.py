from ast import Sub
from curses.ascii import US
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Group, Message, Subject
from .forms import GroupForm, UserForm

def login_user(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get("username").lower()
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
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured while registering this user account.')

    context = {"page": page, "form": form}
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
    subjects = Subject.objects.all()[0:5] # only get the first 5 subjects
    group_messages = Message.objects.filter(Q(group__subject__name__icontains=q))

    context = {"groups": groups, "subjects": subjects, "group_count": group_count, "group_messages": group_messages}
    return render(request, 'base/home.html', context)

def group(request, pk):
    group = Group.objects.get(id=pk)
    group_messages = group.message_set.all()
    members = group.members.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            group=group,
            message=request.POST.get('message')
        )
        group.members.add(request.user)
        return redirect('group', pk=group.id)

    context = {"group": group, "group_messages": group_messages, "members": members}
    return render(request, 'base/group.html', context)

@login_required(login_url='login')
def create_group(request):
    form = GroupForm()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        subject_name = request.POST.get("subject")
        subject, is_created = Subject.objects.get_or_create(name=subject_name)
        Group.objects.create(
            moderator=request.user,
            subject=subject,
            name=request.POST.get("name"),
            description=request.POST.get("description")
        )

        return redirect('home')

    context = {"form": form, "subjects": subjects}
    return render(request, 'base/create_group.html', context)

@login_required(login_url='login')
def update_group(request, pk):
    group = Group.objects.get(id=pk)
    form = GroupForm(instance=group)
    subjects = Subject.objects.all()

    if request.user != group.moderator:
        return HttpResponse('Action not allowed.')

    if request.method == 'POST':
        subject_name = request.POST.get("subject")
        subject, is_created = Subject.objects.get_or_create(name=subject_name)
        group.name = request.POST.get("name")
        group.subject = subject
        group.description = request.POST.get("description")
        group.save()
        return redirect('home')

    context = {"form": form, "subjects": subjects, "group": group}
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

@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Action not allowed.')

    if request.method == "POST":
        message.delete()
        return redirect('home')

    context = {"obj": message}
    return render(request, 'base/delete.html', context)

def user_profile(request, pk):
    user = User.objects.get(id=pk)
    groups = user.group_set.all()
    group_messages = user.message_set.all()
    subjects = Subject.objects.all()

    context = {"user": user, "groups": groups, "group_messages": group_messages, "subjects": subjects}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def update_user_profile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {"form": form}
    return render(request, 'base/update_profile.html', context)

def all_subjects(request):
    q = request.GET.get('q', '')
    subjects = Subject.objects.filter(name__icontains=q)
    context = {"subjects": subjects}
    return render(request, 'base/all_subjects.html', context)

def all_activity(request):
    group_messages = Message.objects.all()
    context = {"group_messages": group_messages}
    return render(request, 'base/all_activity.html', context)