from django.urls import path
from . import  views
from .views import UserCreateView, UserUpdateView, UserDetailView
app_name = 'superadmin'





urlpatterns = [

    path('new_entry/', UserCreateView.as_view(), name='new_entry'),
    path("users/by-department/", views.users_by_department, name="users_by_department"),


    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/detail/', UserDetailView.as_view(), name='user_detail'),
    path('home/', views.index,name='dashboard' ),
    path('ana_distribution/', views.distribution,name='ana_distribution' ),
    path('ana_movement/', views.movement,name='ana_movement' ),
    path('ana_training/', views.training,name='ana_training' ),
    path('all_users/', views.all_users,name='all_users' ),


]
