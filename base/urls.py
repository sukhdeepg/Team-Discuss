from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('group/<str:pk>/', views.group, name="group"),
    path('create-group/', views.create_group, name="create-group"),
    path('update-group/<str:pk>/', views.update_group, name="update-group"),
    path('delete-group/<str:pk>/', views.delete_group, name="delete-group"),
    path('delete-message/<str:pk>/', views.delete_message, name="delete-message"),
    path('profile/<str:pk>/', views.user_profile, name="profile"),
    path('update-profile/', views.update_user_profile, name="update-profile"),
    path('all-subjects/', views.all_subjects, name="all-subjects"),
    path('all-activity/', views.all_activity, name="all-activity")
]
