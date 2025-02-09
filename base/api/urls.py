from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('groups/', views.get_groups),
    path('group/<str:pk>/', views.get_group)
]
