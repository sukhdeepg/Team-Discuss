from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('group/<str:pk>/', views.group, name="group")
]
