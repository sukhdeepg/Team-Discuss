from django.shortcuts import render

def home(request):
    return render(request, 'base/home.html')

def group(request, pk):
    return render(request, 'base/group.html')